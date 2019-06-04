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

#### [framework/logger.py](./../networking_test/framework/logger.py)
Logger class, to register test steps and display them in result of tests running. 

#### [framework/color_text.py](./../networking_tests/framework/color_text.py)
Helper functions for color text making.

#### [framework/utils.py](./../networking_tests/framework/utils.py)
Some default variables.

## Example tests

The [example tests](./../networking_tests/) were heavily commented. If you are writing your first test, copy one of them and modify to fit your needs.

## Test properties

You can set test properties when initialize it, for fine tuning:

- `node_count: integer` - count of nodes in network.
- `connection_mode: string` - type of nodes connection. Can be: 'all', 'chain', None .
- `account_count: integer` - number of accounts in network.
- `account authorization: list` - each element is number of node on which corresponding account would be authorized (correspondance condition = index of element).
- `asset_distribution_type: string` - type of asset distribution between accounts in account generation process. Can be: 'random', 'equal', 'fixed'.

Each test obtain properties, automated setted using `config.py`:

- `api_access: string` - path to api-access config file.
- `data_dir: string` - path to desired data directory.
- `node_path: string` - path to echo node.

In test properties you can find objects:

- `echopy:` [EchopyWrapper](./../networking_tests/framework/echopy_wrapper.py) object - to easy using the API and building/sending a transaction. This object have methods to easy generate [account](./../networking_tests/framework/objects.py)(s).
- `genesis:` [GenesisConfig](./../networking_tests/framework/objects.py) object - to easy access of genesis configuration file.
- `log:` [Logger](./../networking_tests/framework/logger.py) object - provides logging methods. All logs are include in results ot `test_runner.py` script.

For each echo-node when test running makes a Node object:

- `nodes: list` - each element is object of [Node](./../networking_tests/framework/node.py) class.

You can define new properties required to specific test.


## General test-writing advice

- Set custom config parameters for running tests in `config.py` file.
- Make <YourTestName> class that inherit `EchoTest`.
- Use `block_timeout_callback` and `block_interval_callback` decorators to functions, that define logic of test.
- Use `finalize` flag in `block_timeout_callback` decorator, if this function assert conditions to make test done. You can use many functions with `finalize` flag.
- Use `log` property of `EchoTest` class to make logs in test, which display in full log-result of tests running.
- Override `setup` method in test. Run all logic functions in it.
