import string
import random

from echopy import Echo
from echopy.echobase.account import PrivateKey

from .node import Node
from .objects import Account, AssetDistribution, EqualDistribution, RandomDistribution, FixedDistribution
from .utils import ASSET_DISTRIBUTION_TYPES, DEFAULT_ASSET_DISTRIBUTION_TYPE,\
    DEFAULT_ASSET_TOTAL_AMOUNT, DEFAULT_ASSET_SYMBOL


class EchopyWrapper(Echo):
    def __init__(self):
        super().__init__()

    def connect(self, node):
        assert isinstance(node, (str, Node))
        url = 'ws://127.0.0.1:{}'.format(node.rpc_port)
        self.api.connect(node) if isinstance(node, str) else self.api.connect(url)

    def generate_account(self, name=None, private_key=None, public_key=None, lifetime_status=True,
                         asset_amount=None, asset_symbol=DEFAULT_ASSET_SYMBOL):
        if not name:
            name = "".join(random.choice(string.ascii_lowercase) for i in range(random.randint(5, 10)))

        if not public_key and private_key:
            private_key_object = PrivateKey(private_key)
            public_key = str(private_key_object.pubic_key)
        elif not public_key and not private_key:
            brain_key = self.brain_key()
            private_key = brain_key.get_private_key_base58()
            public_key = brain_key.get_public_key_base58()

        account_args = {'name': name, 'lifetime_status': lifetime_status,
                        'public_key': public_key, 'private_key': private_key}

        if asset_amount:
            account_args.update({'asset_amount': asset_amount, 'asset_symbol': asset_symbol})

        return Account(**account_args)

    def generate_accounts(self, count, asset_distribution_type=[DEFAULT_ASSET_DISTRIBUTION_TYPE],
                          asset_amount=[DEFAULT_ASSET_TOTAL_AMOUNT], asset_symbol=[DEFAULT_ASSET_SYMBOL]):

        if not isinstance(asset_distribution_type, list):
            asset_distribution_type = [asset_distribution_type]

        if not isinstance(asset_amount, list):
            asset_amount = [asset_amount]

        if not isinstance(asset_symbol, list):
            asset_symbol = [asset_symbol]

        assert count
        accounts = [self.generate_account() for _ in range(count)]

        for asset_num, asset_distribution in enumerate(asset_distribution_type):

            assert isinstance(asset_distribution, (AssetDistribution, str))

            if isinstance(asset_distribution, str) and asset_distribution in ASSET_DISTRIBUTION_TYPES:
                if asset_distribution == 'equal':
                    distribution = EqualDistribution(count, asset_amount[asset_num])
                elif asset_distribution == 'random':
                    distribution = RandomDistribution(count, asset_amount[asset_num])
                elif asset_distribution == 'fixed':
                    distribution = FixedDistribution(count, asset_amount[asset_num])

            elif isinstance(asset_distribution, AssetDistribution):
                if asset_distribution_type.count > count:
                    raise Exception('AssetDistribution object have count value more than accounts count')
                distribution = asset_distribution

            else:
                raise Exception('For custom asset distibutions use AssetDistribution class objects')

            assets = distribution.get_assets()
            for account_num, asset in enumerate(assets):
                accounts[account_num].add_initial_balance(asset, asset_symbol[asset_num])

        return accounts
