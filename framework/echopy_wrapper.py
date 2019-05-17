import string
import random

from echopy import Echo
from echopy.echobase.account import PrivateKey
from objects import Account, AssetDistribution, EqualDistribution, RandomDistribution, FixedDistribution

from utils import ASSET_DISTRIBUTION_TYPES, DEFAULT_ASSET_DISTRIBUTION_TYPE, DEFAULT_ASSET_TOTAL_AMOUNT, DEFAULT_ASSET_SYMBOL


class EchopyWrapper:
    def __init__(self):
        self.echopy = Echo()

    def generate_account(self, name=None, private_key=None, public_key=None, lifetime_status=True,
                         asset_amount=None, asset_symbol=DEFAULT_ASSET_SYMBOL):
        if not name:
            name = "".join(random.choice(string.ascii_lowercase) for i in range(random.randint(5, 10)))

        if not public_key and private_key:
            private_key_object = PrivateKey(private_key)
            public_key = str(private_key_object.pubic_key)
        elif not public_key and not private_key:
            brain_key = self.echopy.brain_key()
            private_key = brain_key.get_private_key_base58()
            public_key = brain_key.get_public_key_base58()

        account_args = {'name': name, 'lifetime_status': lifetime_status,
                        'public_key': public_key, 'private_key': private_key}

        if asset_amount:
            account_args.update({'asset_amount': asset_amount, 'asset_symbol': asset_symbol})

        return Account(**account_args)

    def generate_accounts(self, count, asset_distribution_type=DEFAULT_ASSET_DISTRIBUTION_TYPE,
                          asset_amount=DEFAULT_ASSET_TOTAL_AMOUNT, asset_symbol=DEFAULT_ASSET_SYMBOL):

        assert len(count)
        assert isinstance(asset_distribution_type, [AssetDistribution, str])

        if isinstance(asset_distribution_type, str):
            if asset_distribution_type == 'equal':
                distribution = EqualDistribution(count, asset_amount)
            elif asset_distribution_type == 'random':
                distribution = RandomDistribution(count, asset_amount)
            elif asset_distribution_type == 'fixed':
                distribution = FixedDistribution(count, asset_amount)
            else:
                raise Exception('For custom asset distibutions use AssetDistribution class objects')

        elif isinstance(ass)


            for account in accounts:
                account.add_initial_balance(asset_amount, self.asset_symbol)












    def distribute_asset(self, accounts):
        assert len(accounts)

        if self.asset_distribution_type == 'equal':
            asset_amount = self.asset_amount // len(accounts)
            for account in accounts:
                account.add_initial_balance(asset_amount, self.asset_symbol)
        elif self.asset_distribution_type == 'random':
            for account in accounts:
                asset_amount = randint(0, self.asset_amount)
                account.add_initial_balance(asset_amount, self.asset_symbol)
        elif self.asset_distribution_type == 'fixed':
            if not isinstance(self.asset_amount, list):
                self.asset_amount = list(self.asset_amount)

            assert len(self.asset_amount) <= len(accounts)

            for account_num, asset_amount in enumerate(self.asset_amount):
                accounts[account_num].add_initial_balance(asset_amount, self.asset_symbol)

        return accounts
