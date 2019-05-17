import json
import os
import time
from random import randint
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

        self._system_genesis_path = DEFAULT_SYSTEM_GENESIS_PATH
        os.makedirs(self._system_genesis_path[:self._system_genesis_path.rfind('/')], exist_ok=True)

        self.genesis = GenesisConfig()
        self.genesis.generate_from_node(node_path=self.node_path, path_to_save=self._system_genesis_path)
        self.genesis.load_from_file(self._system_genesis_path)

        self.echopy = EchopyWrapper()

    def _initialize_network(self):
        self.nodes = []
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
                account_args = {}
                account_args.update({'name': account_info['name']})
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

    def start_network(self):
        self._initialize_network()
        self._read_accounts_info()
        for node in self.nodes:
            node.start()

        time.sleep(1)
        self.genesis.save_to_file(self.genesis_path)

    def stop_network(self):
        for node in self.nodes:
            node.stop()
