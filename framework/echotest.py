import json
import os
import shutil
import time
from functools import partial
from .objects import Account, GenesisConfig
from .node import Node
from .utils import DEFAULT_DATA_DIR, DEFAULT_NETWORK_NODE_COUNT, DEFAULT_NETWORK_CONNECTION_MODE, \
    NETWORK_CONNECTION_MODES, DEFAULT_ASSET_DISTRIBUTION_TYPE, ASSET_DISTRIBUTION_TYPES, \
    DEFAULT_ASSET_TOTAL_AMOUNT, DEFAULT_ACCOUNT_COUNT, DEFAULT_ASSET_SYMBOL, \
    DEFAULT_GENESIS_PATH, DEFAULT_SYSTEM_GENESIS_PATH
from .echopy_wrapper import EchopyWrapper


class EchoTest:

    def __init__(self):
        assert self.node_path
        assert self.api_access

        if not hasattr(self, 'genesis_path'):
            self.genesis_path = DEFAULT_GENESIS_PATH

        if not hasattr(self, 'data_dir'):
            self.data_dir = DEFAULT_DATA_DIR

        if not hasattr(self, 'node_count'):
            self.node_count = DEFAULT_NETWORK_NODE_COUNT

        if not hasattr(self, 'connection_mode') or self.connection_mode not in NETWORK_CONNECTION_MODES:
            self.connection_mode = DEFAULT_NETWORK_CONNECTION_MODE

        if not hasattr(self, 'account_count'):
            self.account_count = DEFAULT_ACCOUNT_COUNT

        if not hasattr(self, 'asset_distribution_type') or \
                self.asset_distribution_type not in ASSET_DISTRIBUTION_TYPES:
                    self.asset_distribution_type = DEFAULT_ASSET_DISTRIBUTION_TYPE

        if not hasattr(self, 'asset_amount'):
            self.asset_amount = DEFAULT_ASSET_TOTAL_AMOUNT

        if not hasattr(self, 'asset_symbol'):
            self.asset_symbol = DEFAULT_ASSET_SYMBOL

        if hasattr(self, 'account_authorization'):
            assert len(self.account_authorization) <= self.account_count
            assert max(self.account_authorization) < self.node_count
            assert min(self.account_authorization) >= 0
        else:
            self.account_authorization = []

        self._system_genesis_path = DEFAULT_SYSTEM_GENESIS_PATH
        os.makedirs(self._system_genesis_path[:self._system_genesis_path.rfind('/')], exist_ok=True)

        self.genesis = GenesisConfig()
        self.genesis.generate_from_node(node_path=self.node_path, path_to_save=self._system_genesis_path)
        self.genesis.load_from_file(self._system_genesis_path)

        self.nodes = []
        self.echopy = EchopyWrapper()

        self._done = False
        self._status = None

    def _initialize_network(self):
        seed_node_arguments = [[] for _ in range(self.node_count)]

        if self.connection_mode == 'all':
            for i in range(self.node_count):
                for j in range(self.node_count):
                    if i != j:
                        seed_node_arguments[i].append(j)

        elif self.connection_mode == 'chain':
            for i in range(self.node_count):
                if i == 0:
                    seed_node_arguments[i].append(self.node_count - 1)
                else:
                    seed_node_arguments[i].append(i - 1)

        for node_num in range(self.node_count):
            self.nodes.append(Node(node_path=self.node_path, genesis_path=self.genesis_path,
                                   api_access=self.api_access, data_dir=self.data_dir,
                                   node_num=node_num, seed_nodes=seed_node_arguments[node_num]))

    def _read_accounts_info(self):
        self.accounts = []
        self.genesis.save_to_file(self._system_genesis_path)
        with open(self._system_genesis_path, 'r') as file:
            genesis_config = json.loads(file.read())
            initial_balances = {initial_balance["owner"]: [
                initial_balance["amount"], initial_balance["asset_symbol"]]
                for initial_balance in genesis_config['initial_balances']}
            for account_num, account_info in enumerate(genesis_config['initial_accounts']):
                name = account_info['name']
                if 'init' not in name and name != 'nathan':
                    account_args = {}
                    account_args.update({'name': name})
                    account_args.update({'account_id': '1.2.{}'.format(6 + account_num)})
                    account_args.update({'lifetime_status': account_info['is_lifetime_member']})
                    account_args.update({'public_key': account_info['active_key']})
                    if account_args['public_key'] in initial_balances:
                        account_args.update({'asset_amount':
                                            initial_balances[account_args['public_key']][0]})
                        account_args.update({'asset_symbol':
                                            initial_balances[account_args['public_key']][1]})
                    if 'private_key' in account_info:
                        account_args.update({'private_key': account_info['private_key']})

                    self.accounts.append(Account(**account_args))

    def _authorize_accounts(self):
        for node in self.nodes:
            for account_num, authorization_node in enumerate(self.account_authorization):
                if node.node_num == authorization_node:
                    node.authorize_account(self.accounts[account_num])
                    self.accounts[account_num].authorized_node = node.node_num

    def _start_nodes(self):
        for node in self.nodes:
            if not node.node_num and os.path.exists(self.data_dir):
                shutil.rmtree(self.data_dir)
            data_dir = '{}/node{}'.format(self.data_dir, node.node_num)
            os.makedirs(data_dir)
            with open('{}/config.ini'.format(data_dir), 'a+') as file:
                for account_num, node_num in enumerate(self.account_authorization):
                    if node.node_num == node_num:
                        account = self.accounts[account_num]
                        account_id = account.id
                        private_key = account.private_key
                        # new_string = 'ed-private-key = ["{}","DET{}"]\n'.format(public_key, private_key)
                        new_string = 'account-info = ["{}","DET{}"]\n'.format(account_id, private_key)
                        file.write(new_string)
                        self.accounts[account_num]

            node.start()

    def main(self):
        """Needed to override."""
        pass

    def _start_network(self):
        self._initialize_network()
        self._read_accounts_info()
        self._authorize_accounts()
        self._start_nodes()
        self.genesis.save_to_file(self.genesis_path)
        time.sleep(1.5)
        self.echopy.connect(self.nodes[0])  # Default connection to first node
        self._run_callbacks()

    def _stop_network(self):
        for node in self.nodes:
            node.stop()

    def run(self):
        if hasattr(self, 'main'):
            self.main()
        self._start_network()
        self._stop_network()

    def _update_block_head_num(self):
        actual_head_block_num = self.echopy.api.database.get_dynamic_global_properties()['head_block_number']
        if actual_head_block_num > self._head_block_num:
            self._head_block_num = actual_head_block_num
            return True
        return False

    def _run_callbacks(self):
        def check_finalize_status(finalize_results):
            if None in finalize_results:
                for result_num, result in enumerate(finalize_results):
                    finalize_results[result_num] = True if result is None else bool(result)

            return False if False in finalize_results else True

        def run_callback(callback):
            assertion_error = None
            try:
                callback()
            except AssertionError as assertion_error:
                pass

            if assertion_error:
                assertion_error = 'AssertionError: {}'.format(assertion_error)

            return assertion_error

        has_finalize_callbacks = hasattr(self, '_finalize_callbacks')
        has_timeout_callbacks = hasattr(self, '_timeout_callbacks')
        has_interval_callbacks = hasattr(self, '_interval_callbacks')
        assert has_finalize_callbacks
        needed_total_agrees = sum([len(self._finalize_callbacks[x]) for x in self._finalize_callbacks])
        if has_timeout_callbacks or has_interval_callbacks:
            self._head_block_num = 0
            while True:
                time.sleep(1)

                if self._update_block_head_num():

                    if has_timeout_callbacks:
                        if self._head_block_num in self._timeout_callbacks:
                            for callback in self._timeout_callbacks[self._head_block_num]:
                                callback()

                    if has_interval_callbacks:
                        for block_delimiter in self._interval_callbacks:
                            if not self._head_block_num % block_delimiter and self._head_block_num > 0:
                                for callback in self._interval_callbacks[block_delimiter]:
                                    callback()

                    for block_num in self._finalize_callbacks:
                        if self._head_block_num in self._finalize_callbacks:
                            for callback in self._finalize_callbacks[self._head_block_num]:
                                self._finalize_results.append(run_callback(callback))

                    if len(self._finalize_results) == needed_total_agrees:
                        self._done = True
                        self._status = check_finalize_status(self._finalize_results)

                if self._done:
                    break

    @staticmethod
    def block_timeout_callback(block_num, finalize=False):

        def inner_function(function):

            def add_callback(*args):
                if finalize:
                    if not hasattr(args[0], '_finalize_callbacks'):
                        args[0]._finalize_callbacks = {}
                        args[0]._finalize_results = []

                    if block_num not in args[0]._finalize_callbacks:
                        args[0]._finalize_callbacks.update({block_num: []})
                    args[0]._finalize_callbacks[block_num].append(partial(function, args))
                else:
                    if not hasattr(args[0], '_timeout_callbacks'):
                        args[0]._timeout_callbacks = {}

                    if block_num not in args[0]._timeout_callbacks:
                        args[0]._timeout_callbacks.update({block_num: []})
                    args[0]._timeout_callbacks[block_num].append(partial(function, args))

            return add_callback
        return inner_function

    @staticmethod
    def block_interval_callback(block_num):

        def inner_function(function):

            def add_callback(*args):
                if not hasattr(args[0], '_interval_callbacks'):
                    args[0]._interval_callbacks = {}

                if block_num not in args[0]._interval_callbacks:
                    args[0]._interval_callbacks.update({block_num: []})
                args[0]._interval_callbacks[block_num].append(partial(function, args))

            return add_callback
        return inner_function
