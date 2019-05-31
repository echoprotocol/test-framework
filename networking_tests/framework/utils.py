STARTING_RPC_PORT = 8090
STARTING_P2P_PORT = 13375
GENERATE_GENESIS_NODE_NUM = 1000

DEFAULT_TEMP_PATH = './.tmp'

NETWORK_CONNECTION_MODES = ['all', 'chain', None]
DEFAULT_NETWORK_CONNECTION_MODE = 'all'

ASSET_DISTRIBUTION_TYPES = ['random', 'fixed', 'equal']
DEFAULT_ASSET_DISTRIBUTION_TYPE = 'equal'

DEFAULT_ASSET_SYMBOL = 'ECHO'
DEFAULT_ASSET_ID = '1.3.0'

DEFAULT_NETWORK_NODE_COUNT = 2
DEFAULT_ACCOUNT_COUNT = 0

DEFAULT_GENESIS_ECHORAND_CONFIG = {
    "_time_net_1mb": 3000,
    "_time_net_256b": 1500,
    "_creator_count": 2,
    "_verifier_count": 7,
    "_ok_threshold": 5,
    "_max_bba_steps": 12
}

DEFAULT_GENESIS_SIDECHAIN_CONFIG = {
    "eth_contract_address": "22ff2e2c3c7015d4948073742d6e3c50d4d8c55f",
    "eth_committee_update_method": {
        "method": "ffffffff",
        "gas": 1000000
    },
    "eth_gen_address_method": {
        "method": "ffcc34fd",
        "gas": 1000000
    },
    "eth_withdraw_method": {
        "method": "e21bd1ce",
        "gas": 1000000
    },
    "eth_committee_updated_topic": "514bf7702a7d2aca90dcf3d947158aad29563a17c1dbdc76d2eae84c22420142",
    "eth_gen_address_topic": "1855f12530a368418f19b2b15227f19225915b8113c7e17d4c276e2a10225039",
    "eth_deposit_topic": "77227a376c41a7533c952ebde8d7b44ee36c7a6cec0d3448f1a1e4231398356f",
    "eth_withdraw_topic": "481c4276b65cda86cfcd095776a5e290a13932f5bed47d4f786b0ffc4d0d76ae",
    "ETH_asset_id": "1.3.1"
}
