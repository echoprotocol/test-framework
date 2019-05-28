import os
import subprocess
from .utils import STARTING_RPC_PORT, STARTING_P2P_PORT, DEFAULT_TEMP_PATH


class Node:

    def __init__(self, node_path=None, genesis_path=None, api_access=None,
                 node_num=0, seed_nodes=None, accounts_info=None,
                 committee_accounts=None, data_dir=None, start_echorand=False):

        self.node_path = node_path
        self.node_num = node_num
        self.rpc_port = STARTING_RPC_PORT + self.node_num
        self.p2p_port = STARTING_P2P_PORT + self.node_num
        self.seed_nodes = seed_nodes
        self.genesis_path = genesis_path
        self.api_access = api_access
        self.data_dir = data_dir
        self.authorized_command = ''
        self._start_echorand = start_echorand

    @property
    def node_path(self):
        if not self._node_path:
            raise("'node path' is needed")
        return self._node_path

    @node_path.setter
    def node_path(self, node_path):
        self._node_path = node_path

    @property
    def genesis_path(self):
        if not self._genesis_path:
            raise("'genesis_path' is needed")
        return self._genesis_path

    @genesis_path.setter
    def genesis_path(self, genesis_path):
        self._genesis_path = genesis_path

    @property
    def api_access(self):
        if not self._api_access:
            raise("'api_access' is needed")
        return self._api_access

    @api_access.setter
    def api_access(self, api_access):
        self._api_access = api_access

    def generate_genesis(self, path_to_save):
        if not self.node_path:
            raise("'node path' is needed")

        if not path_to_save:
            raise ("'path_to_save' is needed")

        if os.path.exists(path_to_save):
            os.remove(path_to_save)

        command = 'screen -S node{} -d -m {}'.format(self.node_num, self.node_path)
        command += ' --create-genesis-json {}'.format(path_to_save)
        subprocess.Popen(command, shell=True)

    def authorize_account(self, account):
        self.authorized_command += ' --account-info \[\\\"{}\\\",\\\"DET{}\\\"\]'.format(account.id,
                                                                                         account.private_key)

    def start(self):

        if self.seed_nodes is not None and not isinstance(self.seed_nodes, list):
            self.seed_nodes = [self.seed_nodes]

        data_dir = '{}/node{}'.format(self.data_dir, self.node_num)
        command = '{} --echorand'.format(self.node_path)
        command += ' --rpc-endpoint=127.0.0.1:{} --p2p-endpoint=127.0.0.1:{}'.format(self.rpc_port, self.p2p_port)
        command += ' --data-dir={} --genesis-json {} --api-access {}'.format(data_dir, self.genesis_path,
                                                                             self.api_access)

        if self.authorized_command:
            command += self.authorized_command

        if self.seed_nodes:
            for seed_node in self.seed_nodes:
                if seed_node < STARTING_P2P_PORT:
                    seed_node += STARTING_P2P_PORT
                command += ' --seed-node=127.0.0.1:{}'.format(seed_node)
        if self._start_echorand:
            command += ' --start-echorand'

        runfile_path = '{}/run{}.sh'.format(DEFAULT_TEMP_PATH, self.node_num)
        with open(runfile_path, 'w') as file:
            file.write(command)

        subprocess.Popen('screen -S node{} -d -m bash {}'.format(self.node_num, runfile_path), shell=True)

    def stop(self):
        subprocess.call('screen -x node{} -X quit'.format(self.node_num), shell=True)
