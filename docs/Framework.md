# Framework

## Framework modules

#### [framework/echotest.py](./../networking_tests/framework/echotest.py)
Base class for test.

#### [framework/echopy_wrapper.py](./../networking_tests/framework/echopy_wrapper.py)
Wrapper class of [echopy-lib](https://github.com/echoprotocol/echopy-lib) for : using the API, building/sending a transaction.

#### [framework/node.py](./../networking_tests/framework/node.py)
Basic class for echo-node management.

#### [framework/objects.py](./../networking_tests/framework/objects.py)
Helper objects, like `GenesisConfig`, `Account` and etc.

#### [framework/callbacks.py](./../networking_tests/framework/callbacks.py)
Callback functions, that help to set block-timeout or rule of block-interval for running functions in tests.

#### [framework/color_text.py](./../networking_tests/framework/color_text.py)
Helper functions for color text making.

#### [framework/utils.py](./../networking_tests/framework/utils.py)
Some default variables.

## Example tests

The [example tests](./../networking_tests/) were heavily commented. If you are writing your first test, copy one of them and modify to fit your needs.

## General test-writing advice

- Set custom config parameters for running tests in `config.py` file.
- Make <YourTestName> class that inherit `EchoTest` class, you need to override `setup` method.
- Use `block_timeout_callback` and `block_interval_callback` decorators to functions, that define logic of test.
- Use `finalize` flag in `block_timeout_callback` decorator, if this function assert conditions to make test done. You can use many functions with `finalize` flag.

