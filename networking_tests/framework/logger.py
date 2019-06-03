from textwrap import TextWrapper
from .color_text import text_info, text_warn, text_fail


class Logger:

    def __init__(self):
        self._logs = []

    def debug(self, msg):
        self._logs.append(['{} {}'.format('[DEBUG]', msg), text_info])

    def info(self, msg):
        self._logs.append(['{} {}'.format('[INFO]', msg), text_info])

    def warning(self, msg):
        self._logs.append(['{} {}'.format('[WARNING]', msg), text_warn])

    def error(self, msg):
        self._logs.append(['{} {}'.format('[ERROR]', msg), text_fail])

    def critical(self, msg):
        self._logs.append(['{} {}'.format('[CRITICAL]', msg), text_fail])

    def get_logger_steps(self, width=70):
        wrapper = TextWrapper(width=width)
        return [color(msg_part).ljust(width) for msg, color in self._logs for msg_part in wrapper.wrap(msg)]
