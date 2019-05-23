from functools import partial


def block_timeout_callback(block_num, finalize=False):

    def inner_function(function):

        def add_callback(*args):
            if finalize:
                if not hasattr(args[0], '_finalize_callbacks'):
                    args[0]._finalize_callbacks = {}
                    args[0]._finalize_results = []

                if block_num not in args[0]._finalize_callbacks:
                    args[0]._finalize_callbacks.update({block_num: []})
                args[0]._finalize_callbacks[block_num].append(partial(function, *args))
            else:
                if not hasattr(args[0], '_timeout_callbacks'):
                    args[0]._timeout_callbacks = {}

                if block_num not in args[0]._timeout_callbacks:
                    args[0]._timeout_callbacks.update({block_num: []})
                args[0]._timeout_callbacks[block_num].append(partial(function, *args))

        return add_callback
    return inner_function


def block_interval_callback(block_num):

    def inner_function(function):

        def add_callback(*args):
            if not hasattr(args[0], '_interval_callbacks'):
                args[0]._interval_callbacks = {}

            if block_num not in args[0]._interval_callbacks:
                args[0]._interval_callbacks.update({block_num: []})

            args[0]._interval_callbacks[block_num].append(partial(function, *args))

        return add_callback
    return inner_function
