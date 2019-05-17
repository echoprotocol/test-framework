STARTING_RPC_PORT = 8090
STARTING_P2P_PORT = 13375
GENERATE_GENESIS_NODE_NUM = 1000
DEFAULT_DATA_DIR = './data'
DEFAULT_SYSTEM_GENESIS_PATH = '/tmp/echo_test_framework/genesis.json'
DEFAULT_GENESIS_PATH = '{}/genesis.json'.format(DEFAULT_DATA_DIR)
DEFAULT_NETWORK_NODE_COUNT = 2
NETWORK_CONNECTION_MODES = ['all', 'chain', None]
DEFAULT_NETWORK_CONNECTION_MODE = 'all'
DEFAULT_ACCOUNT_COUNT = 10
ASSET_DISTRIBUTION_TYPES = ['random', 'fixed', 'equal']
DEFAULT_ASSET_DISTRIBUTION_TYPE = 'equal'
DEFAULT_ASSET_TOTAL_AMOUNT = 1000000000
DEFAULT_ASSET_SYMBOL = 'ECHO'

ECHO_FOLDER = '/home/evasilev/Documents/Projects/echo'
NODE_PATH = '{}/bin/echo_node'.format(ECHO_FOLDER)
API_ACCESS = '{}/access.json'.format(ECHO_FOLDER)


DEFAULT_GENESIS_ECHORAND_CONFIG = {
    "_time_net_1mb": 3000,
    "_time_net_256b": 1500,
    "_creator_count": 2,
    "_verifier_count": 7,
    "_ok_threshold": 5,
    "_max_bba_steps": 12
}

DEFAULT_GENESIS_SIDECHAIN_CONFIG = {
    "echo_contract_id": "1.14.0",
    "echo_vote_method": "7d310fba",
    "echo_sign_method": "224e89de",
    "echo_transfer_topic": "74c980d5dc214f02ed77d4e6c85f839efa386f2fb2f08a7102eb27b72316b7d0",
    "echo_transfer_ready_topic": "b13dc7ed3b922a635e7756f98f1404ed221e7977cb0fbe7ad5ca1a8c0de7ed89",
    "eth_contract_address": "ee7d89dbe8aaafbd1f5e7adc9992b66ad4076029",
    "eth_committee_method": "ffffffff",
    "eth_transfer_topic": "514bf7702a7d2aca90dcf3d947158aad29563a17c1dbdc76d2eae84c22420142"
}
