import os
import subprocess
import signal
from .utils import STARTING_RPC_PORT, STARTING_P2P_PORT


class Node:

    def __init__(self, node_path=None, genesis_path=None, api_access=None,
                 node_num=0, seed_nodes=None, accounts_info=None,
                 committee_accounts=None, data_dir=None):

        self.node_path = node_path
        self.node_num = node_num
        self.rpc_port = STARTING_RPC_PORT + self.node_num
        self.p2p_port = STARTING_P2P_PORT + self.node_num
        self.seed_nodes = seed_nodes
        self.accounts_info = accounts_info  # TODO
        self.committee_accounts = committee_accounts  # TODO
        self.genesis_path = genesis_path
        self.api_access = api_access
        self.data_dir = data_dir
        self.authorized_command = ''

    def generate_genesis(self, path):
        if not self.node_path:
            raise("'node path' is needed")

        if not path:
            raise ("'path_to_save' is needed")

        if os.path.exists(path):
            os.remove(path)

        command = 'screen -S node{} -d -m {}'.format(self.node_num, self.node_path)
        command += ' --create-genesis-json {}'.format(path)

        subprocess.Popen(command, shell=True)

    def authorize_account(self, account):
        self.authorized_command += ' --account-info \[\\\"{}\\\",\\\"{}\\\"\]'.format(account.id,
                                                                                      account.private_key)

    def start(self):
        if not self.node_path:
            raise("'node path' is needed")

        if not self.genesis_path:
            raise("'genesis_path' is needed")

        if not self.api_access:
            raise("'api_access' is needed")

        if self.seed_nodes is not None and not isinstance(self.seed_nodes, list):
            self.seed_nodes = [self.seed_nodes]

        data_dir = '{}/node{}'.format(self.data_dir, self.node_num)

        command = 'screen -S node{} -d -m {} --echorand'.format(self.node_num, self.node_path)
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
        command += ' --start-echorand --resync-blockchain'
        subprocess.Popen(command, shell=True)

    def stop(self):
        out, _ = subprocess.Popen(['screen', '-list'], stdout=subprocess.PIPE).communicate()
        out = str(out, encoding='utf-8')
        if 'node{}\t'.format(self.node_num) not in out:
            raise Exception('There is no connection')
        end_index = out.find('node{}\t'.format(self.node_num)) - 1
        start_index = out[:end_index].rfind('\t') + 1
        pid = int(out[start_index: end_index])
        os.kill(pid, signal.SIGKILL)
        subprocess.Popen(['screen', '-wipe'], stdout=subprocess.PIPE)
