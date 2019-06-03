import json
import os
import shutil
from time import sleep
from datetime import datetime
from .logger import Logger
from .callbacks import block_timeout_callback
from .objects import GenesisConfig, AssetDistribution
from .node import Node
from .utils import DEFAULT_NETWORK_CONNECTION_MODE, NETWORK_CONNECTION_MODES,\
    DEFAULT_ASSET_DISTRIBUTION_TYPE, ASSET_DISTRIBUTION_TYPES, \
    DEFAULT_ACCOUNT_COUNT, DEFAULT_ASSET_ID, DEFAULT_TEMP_PATH, DEFAULT_NETWORK_NODE_COUNT
from .echopy_wrapper import EchopyWrapper


def timestamp_to_datetime(timestamp):
    return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')


class EchoTest:

    def __init__(self):
        self._temp_genesis_path = '{}/genesis.json'.format(DEFAULT_TEMP_PATH)
        os.makedirs(self._temp_genesis_path[:self._temp_genesis_path.rfind('/')], exist_ok=True)

        self.genesis = GenesisConfig()

        self._done = False
        self._status = None

        self.nodes = []
        self.echopy = EchopyWrapper()
        self.log = Logger()

    @property
    def node_path(self):
        if not hasattr(self, '_node_path'):
            raise Exception('"node_path" property is required')
        return self._node_path

    @node_path.setter
    def node_path(self, node_path):
        self._node_path = node_path

    @property
    def api_access(self):
        if not hasattr(self, '_api_access'):
            raise Exception('"api_access" property is required')
        return self._api_access

    @api_access.setter
    def api_access(self, api_access):
        self._api_access = api_access

    @property
    def data_dir(self):
        if not hasattr(self, '_data_dir'):
            raise Exception('"data_dir" property is required')
        return self._data_dir

    @data_dir.setter
    def data_dir(self, data_dir):
        self._data_dir = data_dir
        self._genesis_path = '{}/genesis.json'.format(self.data_dir)

    @property
    def node_count(self):
        if not hasattr(self, '_node_count'):
            self._node_count = DEFAULT_NETWORK_NODE_COUNT
        return self._node_count

    @node_count.setter
    def node_count(self, node_count):
        self._node_count = node_count

    @property
    def connection_mode(self):
        if not hasattr(self, '_connection_mode') or self._connection_mode not in NETWORK_CONNECTION_MODES:
            self._connection_mode = DEFAULT_NETWORK_CONNECTION_MODE
        return self._connection_mode

    @connection_mode.setter
    def connection_mode(self, connection_mode):
        if connection_mode in NETWORK_CONNECTION_MODES:
            self._connection_mode = connection_mode

    @property
    def account_count(self):
        if not hasattr(self, '_account_count'):
            self.account_count = DEFAULT_ACCOUNT_COUNT
        return self._account_count

    @account_count.setter
    def account_count(self, account_count):
        self._account_count = account_count

    @property
    def asset_distribution_type(self):
        if not hasattr(self, '_asset_distribution_type'):
            self.asset_distribution_type = DEFAULT_ASSET_DISTRIBUTION_TYPE

        return self._asset_distribution_type

    @asset_distribution_type.setter
    def asset_distribution_type(self, asset_distribution_type):
        if asset_distribution_type in ASSET_DISTRIBUTION_TYPES or\
                isinstance(asset_distribution_type, AssetDistribution):
            self._asset_distribution_type = asset_distribution_type

    @property
    def account_authorization(self):
        if not hasattr(self, '_account_authorization'):
            self._account_authorization = []

        return self._account_authorization

    @account_authorization.setter
    def account_authorization(self, account_authorization):
        assert len(account_authorization) <= self.account_count
        assert max(account_authorization) < self.node_count
        assert min(account_authorization) >= 0
        self._account_authorization = account_authorization

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
            node_args = {'node_path': self.node_path, 'genesis_path': self._genesis_path,
                         'api_access': self.api_access, 'data_dir': self.data_dir,
                         'node_num': node_num, 'seed_nodes': seed_node_arguments[node_num]}
            if node_num == self.node_count - 1:
                node_args.update({'start_echorand': True})
            self.nodes.append(Node(**node_args))

    def _read_accounts_info(self):
        self.genesis.save_to_file(self._temp_genesis_path)
        accounts_names = [account.name for account in self.accounts]
        with open(self._temp_genesis_path, 'r') as file:
            genesis_config = json.loads(file.read())
            for account_num, account_info in enumerate(genesis_config['initial_accounts']):
                name = account_info['name']
                account = self.accounts[accounts_names.index(name)]
                account.id = '1.2.{}'.format(6 + account_num)
                account.lifetime_status = account_info['is_lifetime_member']
                account.public_key = account_info['active_key']
                if 'private_key' in account_info:
                    account.private_key = account_info['private_key']

    def _update_accounts_info(self):
        for account in self.accounts:
            if len(account.initial_balances):
                balances = self.echopy.api.database.get_balance_objects([account.public_key])
                for balance in balances:
                    balance_amount = str(balance['balance']['amount'])
                    balance_asset_id = (balance['balance']['asset_id'])
                    for initial_balance in account.initial_balances:
                        first_condition = initial_balance.amount == balance_amount
                        second_condition = initial_balance.asset_id == balance_asset_id
                        if first_condition and second_condition:
                            initial_balance.id = balance['id']

    def _authorize_accounts(self):
        for node in self.nodes:
            for account_num, authorization_node in enumerate(self.account_authorization):
                if node.node_num == authorization_node:
                    node.authorize_account(self.accounts[account_num])
                    self.accounts[account_num].authorized_node = node.node_num

    def _start_nodes(self):
        for node in self.nodes:
            node.start()

    def setup(self):
        """Needed to override."""
        raise NotImplementedError

    def _start_network(self):
        self._initialize_network()
        self._read_accounts_info()
        self._authorize_accounts()
        if os.path.exists(self.data_dir):
            shutil.rmtree(self.data_dir)
        os.makedirs(self.data_dir)
        self.genesis.save_to_file(self._genesis_path)
        self._start_nodes()
        sleep(5)  # TODO: Change to running wait-for-it.sh
        self.echopy.connect(self.nodes[0])  # Default connection to first node
        self._update_accounts_info()
        self._claim_balances()
        self._run_callbacks()

    def _stop_network(self):
        for node in self.nodes:
            node.stop()
        tmp_path = './.tmp'
        if os.path.exists(tmp_path):
            shutil.rmtree(tmp_path)

    def run(self):
        try:
            self.genesis.generate_from_node(node_path=self.node_path, path_to_save=self._temp_genesis_path)
            self.genesis.load_from_file(self._temp_genesis_path)
            self.setup()
            self._start_network()
            self._stop_network()
        except KeyboardInterrupt:
            self._stop_network()

    def _update_block_head(self):
        actual_head_block_num = self.echopy.api.database.get_dynamic_global_properties()['head_block_number']
        if actual_head_block_num > self._head_block_num:
            self._head_block_num = actual_head_block_num
            actual_head_block_time = timestamp_to_datetime(
                self.echopy.api.database.get_block(actual_head_block_num)['timestamp']
            )
            self._head_block_year_diff = actual_head_block_time.year - self._head_block_time.year
            self._head_block_time = actual_head_block_time

            return True
        return False

    def _run_callbacks(self):

        def check_finalize_status(finalize_results):
            return [result if isinstance(result, str) else True for result in finalize_results]

        def run_callback(callback):
            assertion_error = None
            try:
                callback()
            except AssertionError as e:
                assertion_error = "AssertionError: {}".format(e)

            return assertion_error

        has_finalize_callbacks = hasattr(self, '_finalize_callbacks')
        has_timeout_callbacks = hasattr(self, '_timeout_callbacks')
        has_interval_callbacks = hasattr(self, '_interval_callbacks')
        assert has_finalize_callbacks
        needed_total_finalizes = sum([len(self._finalize_callbacks[x]) for x in self._finalize_callbacks])
        if has_timeout_callbacks or has_interval_callbacks:
            self._head_block_num = 0
            self._head_block_time = timestamp_to_datetime('1970-01-01T00:00:00')
            self._head_block_year_diff = 0
            while True:
                sleep(0.5)
                if self._update_block_head():

                    if 0 not in self._timeout_callbacks:
                        if has_timeout_callbacks:
                            if self._head_block_num in self._timeout_callbacks and self._head_block_num > 1:
                                for callback in self._timeout_callbacks[self._head_block_num]:
                                    callback()

                        if has_interval_callbacks:
                            for block_delimiter in self._interval_callbacks:
                                if not self._head_block_num % block_delimiter:
                                    for callback in self._interval_callbacks[block_delimiter]:
                                        callback()

                        for block_num in self._finalize_callbacks:
                            if self._head_block_num in self._finalize_callbacks and self._head_block_num > 1:
                                for callback in self._finalize_callbacks[self._head_block_num]:
                                    self._finalize_results.append(run_callback(callback))

                        if len(self._finalize_results) == needed_total_finalizes:
                            self._done = True
                            self._status = check_finalize_status(self._finalize_results)

                    if self._head_block_year_diff > 0:
                        if has_timeout_callbacks:
                            if 0 in self._timeout_callbacks:
                                for callback in self._timeout_callbacks[0]:
                                    callback()

                                del self._timeout_callbacks[0]

                if self._done:
                    break

    @block_timeout_callback(block_num=0)
    def _claim_balances(self):
        operation_id = self.echopy.config.operation_ids.BALANCE_CLAIM
        tx = self.echopy.create_transaction()
        for account in self.accounts:
            props = {
            }
            for initial_balance in account.initial_balances:
                props = {
                    'deposit_to_account': account.id,
                    'balance_owner_key': account.public_key,
                    "balance_to_claim": initial_balance.id,
                    "total_claimed": {
                        "amount": initial_balance.amount,
                        "asset_id": DEFAULT_ASSET_ID
                    }
                }
                tx.add_operation(operation_id, props)
                tx.add_signer(account.private_key)
        tx.broadcast('1')
