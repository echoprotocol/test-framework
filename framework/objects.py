import json
from random import randint, random
import time
from .utils import DEFAULT_GENESIS_ECHORAND_CONFIG, DEFAULT_GENESIS_SIDECHAIN_CONFIG, GENERATE_GENESIS_NODE_NUM, DEFAULT_ASSET_TOTAL_AMOUNT
from .node import Node


class GenesisConfig:

    def __init__(self, config_path=None):
        if config_path:
            self.load_from_file(path=config_path)

    def generate_from_node(self, node_path, path_to_save):
        node = Node(node_path=node_path, node_num=GENERATE_GENESIS_NODE_NUM)
        node.generate_genesis(path_to_save)

        time.sleep(1)

        with open(path_to_save, 'r') as file:
            genesis_config = json.loads(file.read())

        genesis_config['initial_parameters']['echorand_config'] = DEFAULT_GENESIS_ECHORAND_CONFIG
        genesis_config['initial_parameters']['sidechain_config'] = DEFAULT_GENESIS_SIDECHAIN_CONFIG

        with open(path_to_save, 'w') as file:
            json.dump(genesis_config, file, indent=4)

    def load_from_file(self, path):
        if path:
            with open(path, 'r') as file:
                self.__dict__ = json.loads(file.read())

    def save_to_file(self, path):
        with open(path, 'w') as file:
            json.dump(self.__dict__, file, indent=4)


class Account:

    def __init__(self, name, lifetime_status, public_key, private_key=None, account_id=None,
                 asset_amount=None, asset_symbol='ECHO'):
        self.name = name
        self.id = account_id
        self.lifetime_status = lifetime_status
        self.private_key = private_key
        self.public_key = public_key
        if asset_amount:
            self.initial_balance = InitialBalance(owner=self.public_key,
                                                  amount=asset_amount,
                                                  asset_symbol=asset_symbol)

    @property
    def json(self):
        account_dict = {'name': self.name, 'is_lifetime_member': self.lifetime_status,
                        'active_key': self.public_key, 'ed_key': self.public_key}
        if self.private_key:
            account_dict.update({'private_key': self.private_key})

        return account_dict

    def add_initial_balance(self, amount, asset_symbol='ECHO'):
        if amount:
            self.initial_balance = InitialBalance(owner=self.public_key,
                                                  amount=amount,
                                                  asset_symbol=asset_symbol)


class InitialBalance:

    def __init__(self, owner, amount, asset_symbol='ECHO'):
        if not isinstance(amount, str):
            amount = str(amount)

        self.owner = owner
        self.amount = amount
        self.asset_symbol = asset_symbol

    @property
    def json(self):
        return self.__dict__


class AssetDistribution:
    def __init__(self):
        assert self.count
        assert self.amount

    def get_assets(self):
        pass


class EqualDistribution(AssetDistribution):

    def __init__(self, count, amount):
        self.count = count
        self.amount = amount
        super().__init__()

    def get_assets(self):
        return [int(int(self.amount) // self.count) for _ in range(self.count)]


class RandomDistribution(AssetDistribution):

    def __init__(self, count, amount):
        self.count = count
        self.amount = amount
        super().__init__()

    def get_assets(self):

        def equal_to_random(assets):
            for asset_num, asset in enumerate(assets):
                num = randint(0, len(assets) - 2)
                num = num + 1 if num >= asset_num else num
                assets_sum = asset + assets[num]
                assets[asset_num] = int(random() * assets_sum)
                assets[num] = assets_sum - assets[asset_num]

            return assets

        assets = [int(int(self.amount) // self.count) for _ in range(self.count)]
        return equal_to_random(assets)


class FixedDistribution(AssetDistribution):

    def __init__(self, count, amount):

        if not isinstance(amount, list):
            amount = [amount for _ in range(count)]

        assert len(amount) <= count

        self.count = count
        self.amount = amount
        super().__init__()

    def get_assets(self):
        assets = [None for _ in range(self.count)]
        for asset_num, amount in enumerate(self.amount):
            assets[asset_num] = int(amount)
        return assets
