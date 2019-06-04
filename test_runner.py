import os
import argparse
from inspect import isclass
from glob import glob
from networking_tests.framework.echotest import EchoTest
from networking_tests.framework.color_text import text_bold, text_fail, text_pass
from prettytable import PrettyTable
from config import DATA_DIR, NODE_PATH, API_ACCESS


class TestRunner:

    def __init__(self, test_folder='./networking_tests/'):
        self.test_folder = test_folder
        self.data_dir = os.path.abspath(DATA_DIR)
        self.node_path = os.path.abspath(NODE_PATH)
        self.api_access = os.path.abspath(API_ACCESS)

    @staticmethod
    def _get_import_from_path(path):
        import_path = path[path.find('/') + 1: path.rfind('.py')]
        import_path = import_path.replace('/', '.')
        return import_path

    def _get_test_files(self):
        return glob('{}/*.py'.format(self.test_folder))

    def _get_test_classes(self):
        test_files = self._get_test_files()
        for test in test_files:
            exec('from {} import *'.format(self._get_import_from_path(test)))

        local_objects = locals()
        for _object in local_objects.values():
            if isclass(_object):
                if issubclass(_object, EchoTest):
                    subclasses = _object.__subclasses__()
                    if len(subclasses) >= len(test_files):
                        test_classes = subclasses
        return test_classes

    def _get_logs(self, quiet=False):
        if not quiet:
            status_dict = {True: 'Passed', False: 'Failed'}
            result_log_table = PrettyTable()
            result_log_table.field_names = [text_bold('№'),
                                            text_bold('Test name'),
                                            text_bold('Logs'),
                                            text_bold('Status'),
                                            text_bold('Description')]

            result_log_table.align['Description'] = 'l'
            result_log_table.align['Logs'] = 'l'

        status_counter = {True: 0, False: 0}
        for test_num, logs in enumerate(self._logs):
            status = all([not isinstance(log, str) for log in logs])
            status_counter[status] += 1
            if not quiet:
                description = ''
                if not status:
                    for log in logs:
                        if isinstance(log, str):
                            description += '{}\n'.format(log)
                description = text_fail(description)
                status = text_pass(status_dict[status]) if status else text_fail(status_dict[status])

                for internal_log_num, internal_test_log in enumerate(self._internal_test_logs[test_num]):
                    row = ['' for _ in range(len(result_log_table.field_names))]
                    if not internal_log_num:
                        row = [test_num + 1, self._test_names[test_num], internal_test_log, status, description]
                    row[2] = internal_test_log
                    result_log_table.add_row(row)

                result_log_table.add_row(['' for _ in range(len(result_log_table.field_names))])

        if 'result_log_table' in locals():
            print(result_log_table)
        print('{}: {} | {}: {} | {}: {}'.format(text_bold('Total tests'),
                                                text_bold('{}'.format(len(self._logs))),
                                                text_pass('Passed'),
                                                text_pass('{}'.format(status_counter[True])),
                                                text_fail('Failed'),
                                                text_fail('{}'.format(status_counter[False]))))

    def run_tests(self, quiet=False, logs_width=70):
        tests = self._get_test_classes()
        self._logs = []
        self._internal_test_logs = []
        self._test_names = []
        for test_num, test in enumerate(tests):
            try:
                test_object = test()
                self._test_names.append(test.__name__)
                test_object.data_dir = '{}/{}'.format(self.data_dir, self._test_names[test_num])
                test_object.genesis_path = '{}/genesis.json'.format(test_object.data_dir)
                test_object.node_path = self.node_path
                test_object.api_access = self.api_access

                test_object.run()
                self._internal_test_logs.append(test_object.log.get_logger_steps(logs_width))
                self._logs.append(test_object._status)
            except Exception as e:
                print(e)
        self._get_logs(quiet=quiet)
        print('')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='Run test in quiet mode')
    args = parser.parse_args()

    runner = TestRunner()
    runner.run_tests(quiet=args.quiet)
