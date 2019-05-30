import os
import argparse
from inspect import isclass
from glob import glob
from networking_tests.framework.echotest import EchoTest
from networking_tests.framework.color_text import ColorText
from prettytable import PrettyTable


class TestRunner:

    def __init__(self, test_folder='./networking_tests/', data_dir='./data'):
        self.test_folder = test_folder
        self.data_dir = os.path.abspath(data_dir)

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
            result_log_table.field_names = [ColorText.text_bold('№'),
                                            ColorText.text_bold('Test name'),
                                            ColorText.text_bold('Status'),
                                            ColorText.text_bold('Description')]
            result_log_table.align['Description'] = 'l'

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
                description = ColorText.text_fail(description)
                status = ColorText.text_pass(status_dict[status]) if status else\
                    ColorText.text_fail(status_dict[status])
                result_log_table.add_row([test_num + 1,
                                          self._test_names[test_num],
                                          status,
                                          description
                                          ])
        if 'result_log_table' in locals():
            print(result_log_table, end='\n\n')
        print('{}: {} | {}: {} | {}: {}'.format(ColorText.text_bold('Total tests'),
                                                ColorText.text_bold('{}'.format(len(self._logs))),
                                                ColorText.text_pass('Passed'),
                                                ColorText.text_pass('{}'.format(status_counter[True])),
                                                ColorText.text_fail('Failed'),
                                                ColorText.text_fail('{}'.format(status_counter[False]))))

    def run_tests(self, quiet=False):
        tests = self._get_test_classes()
        self._logs = []
        self._test_names = []
        for test_num, test in enumerate(tests):
            try:
                test_object = test()
                self._test_names.append(test.__name__)
                test_object.data_dir = '{}/{}'.format(self.data_dir, self._test_names[test_num])
                test_object.genesis_path = '{}/genesis.json'.format(test_object.data_dir)
                test_object.run()
                self._logs.append(test_object._status)
            except Exception as e:
                print(e)
        print('')
        self._get_logs(quiet=quiet)
        print('')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='Run test in quiet mode')
    parser.add_argument('-r', '--report', default='', type=str,
                        help='Path for saving log-report')

    args = parser.parse_args()

    runner = TestRunner()
    runner.run_tests(quiet=args.quiet)
