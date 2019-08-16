from .framework.echotest import EchoTest


class InvalidTest(EchoTest):

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
                                                      asset_amount=2000,
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

    def setup(self):
        # Run all callback and others functions in `setup` method
        self.log.info('Run setup')
        self.change_genesis_config()
