# Colored printing functions for strings that use universal ANSI escape sequences.
# fail: bold red, pass: bold green, warn: bold yellow,
# info: bold blue, bold: bold white


class ColorText:

    @staticmethod
    def text_fail(message):
        return '{}{}{}'.format('\x1b[1;31m', message.strip(), '\x1b[0m')

    @staticmethod
    def text_pass(message):
        return '{}{}{}'.format('\x1b[1;32m', message.strip(), '\x1b[0m')

    @staticmethod
    def text_warn(message):
        return '{}{}{}'.format('\x1b[1;33m', message.strip(), '\x1b[0m')

    @staticmethod
    def text_info(message):
        return '{}{}{}'.format('\x1b[1;34m', message.strip(), '\x1b[0m')

    @staticmethod
    def text_bold(message):
        return '{}{}{}'.format('\x1b[1;37m', message.strip(), '\x1b[0m')
