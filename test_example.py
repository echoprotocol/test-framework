from framework.echotest import EchoTest
from framework.utils import NODE_PATH, DEFAULT_GENESIS_PATH, API_ACCESS
from framework.callbacks import block_timeout_callback, block_interval_callback


class ExampleTest(EchoTest):

    def __init__(self):

        # Chain Parameters
        self.node_path = NODE_PATH
        self.genesis_path = DEFAULT_GENESIS_PATH
        self.api_access = API_ACCESS
        self.node_count = 10
        self.connection_mode = 'all'

        # Account parameters
        self.account_count = 30
        self.asset_distribution_type = 'equal'

        result = []
        for i in range(self.node_count):
            result += [i for _ in range(self.account_count // self.node_count)]
        self.account_authorization = result

        super().__init__()

    def make_new_genesis_config(self):
        self.accounts = self.echopy.generate_accounts(count=self.account_count,
                                                      asset_distribution_type=self.asset_distribution_type,
                                                      asset_amount=5000000000,
                                                      asset_symbol='ECHO')
        for _id, account in enumerate(self.accounts):
            self.genesis.initial_accounts.append(account.genesis_account_format)
            self.genesis.initial_committee_candidates.append(account.genesis_committee_format)

            for initial_balance in account.initial_balances:
                self.genesis.initial_balances.append(initial_balance.genesis_format)

    @block_interval_callback(block_num=1)
    def send_transaction(self):
        first_account_num = second_account_num = 14
        second_account_num = 13
        account_from = self.accounts[first_account_num]
        account_to = self.accounts[second_account_num]

        tx = self.echopy.create_transaction()
        transfer_props = {
            'from': account_from.id,
            'to': account_to.id,
            'amount': {
                'asset_id': '1.3.0',
                'amount': 1
            }
        }
        tx.add_operation(self.echopy.config.operation_ids.TRANSFER, transfer_props)
        tx.add_signer(account_from.private_key)
        tx.broadcast('1')

    @block_timeout_callback(block_num=20, finalize=True)
    def n(self):
        print("TIMEOUT")

    def setup(self):
        self.make_new_genesis_config()
        self.send_transaction()
        self.n()
