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
    "_time_generate": 1000,
    "_time_net_1mb": 2000,
    "_time_net_256b": 1500,
    "_creator_count": 2,
    "_verifier_count": 7,
    "_ok_threshold": 5,
    "_max_bba_steps": 12
}


DEFAULT_GENESIS_SIDECHAIN_CONFIG = {
    "eth_contract_address": "cd8a072122aeb5fa749c0c5ce817bbe58111a03d",
    "eth_committee_update_method": {
        "method": "f1e3eb60",
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
    "eth_update_addr_method": {
        "method": "7ff203ab",
        "gas": 1000000
    },
    "eth_withdraw_token_method": {
        "method": "1c69c0e2",
        "gas": 1000000
    },
    "eth_collect_tokens_method": {
        "method": "5940a240",
        "gas": 1000000
    },
    "eth_committee_updated_topic": "514bf7702a7d2aca90dcf3d947158aad29563a17c1dbdc76d2eae84c22420142",
    "eth_gen_address_topic": "1855f12530a368418f19b2b15227f19225915b8113c7e17d4c276e2a10225039",
    "eth_deposit_topic": "77227a376c41a7533c952ebde8d7b44ee36c7a6cec0d3448f1a1e4231398356f",
    "eth_withdraw_topic": "481c4276b65cda86cfcd095776a5e290a13932f5bed47d4f786b0ffc4d0d76ae",
    "erc20_deposit_topic": "d6a701782aaded96fbe10d6bd46445ecef12edabc8eb5d3b15fb0e57f6395911",
    "erc20_withdraw_topic": "ec7288d868c54d049bda9254803b6ddaaf0317b76e81601c0af91a480592b272",
    "ETH_asset_id": "1.3.1",
    "BTC_asset_id": "1.3.2",
    "fines": {
        "generate_eth_address": -10
    },
    "gas_price": 10000000000,
    "satoshis_per_byte": 23,
    "coefficient_waiting_blocks": 100
}

DEBUG_MODE = False
