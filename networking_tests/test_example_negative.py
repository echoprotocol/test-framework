from .framework.echotest import EchoTest
from .framework.callbacks import block_timeout_callback, block_interval_callback


class TestExampleNegative(EchoTest):

    def __init__(self):

        # Chain Parameters
        self.node_count = 10
        self.connection_mode = 'all'

        # Account parameters
        self.account_count = 15
        self.asset_distribution_type = 'equal'
        self.account_authorization = [node_num % self.node_count for node_num in range(self.account_count)]

        super().__init__()

    def change_genesis_config(self):

        self.log.info('Generate accounts')

        # Use echopy method to generate accounts and put it into 'account' property
        self.accounts = self.echopy.generate_accounts(count=self.account_count,
                                                      asset_distribution_type=self.asset_distribution_type,
                                                      asset_amount=5000000000,
                                                      asset_symbol='ECHO')

        self.log.info('Add generated accounts to genesis config')

        # Add all accounts to initial_accounts in genesis.json file
        for _id, account in enumerate(self.accounts):
            # Use account 'genesis_account_format' representation for adding to initial_accounts
            self.genesis.initial_accounts.append(account.genesis_account_format)

            # Add all accounts to initial_committee_candidates in genesis.json file
            # Use account 'genesis_committee_format' representation for adding to inial_committee_candidates
            self.genesis.initial_committee_candidates.append(account.genesis_committee_format)

            # Add all accounts balances to initial_balances in genesis.json file
            # Use initial_balance 'genesis_format' representation for adding to initial_balances
            for initial_balance in account.initial_balances:
                self.genesis.initial_balances.append(initial_balance.genesis_format)

    # Use block_interval_callback to autorun this function through `block_num` blocks count
    @block_interval_callback(block_num=1)
    def send_transaction(self):

        # Use echopy to build and broadcast transaction (transfer operation)
        first_account_num = 13
        second_account_num = 14
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

        # Get number of last block to make understandable logs
        head_block_num = self.echopy.api.database.get_dynamic_global_properties()['head_block_number']
        self.log.info('Block: {} | Transaction broadcasted'.format(head_block_num))

    # Use block_timeout_callback to autorun this function once = when `block_num` block was produced
    # Use finalize flag (default=False) to exit the test after this callback (only for block_timeout_callback)
    @block_timeout_callback(block_num=20, finalize=True)
    def check_last_block(self):
        # Get number of last block
        head_block_num = self.echopy.api.database.get_dynamic_global_properties()['head_block_number']

        # Checks that last block containt at least 3 transactions
        condition = bool(len(self.echopy.api.database.get_block(head_block_num)['transactions']) > 2)
        log_function = self.log.info if condition else self.log.error
        log_function('Finalize condition checked')
        assert condition, 'Last block have small count of transactions (< 3)'

    def setup(self):
        # Run all callback and others functions in `setup` method
        self.log.info('Run setup')
        self.change_genesis_config()
        self.send_transaction()
        self.check_last_block()
