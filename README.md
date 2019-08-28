# Test-Framework for Echo

Test-Framework can be used to test the protocol and network interaction of Echo.

This project does not contain Api/Operations tests, which can be found in <b>[pytests project](https://github.com/echoprotocol/pytests)</b>.

## Installation

### Manual installation:

	$ git clone https://gitlab.pixelplex.by/645.echo/test-framework.git
	$ cd test-framework
	$ pip3 install -r requirements.txt

## Preparation

Locally builded echo node (https://github.com/echoprotocol/echo-core).

## Config

Make copy of config file template, than full needed custom parameters into it:

	$ cp config.py.bak config.py

## Usage

### Run tests

    $ python3 test_runner.py

To check available parameters to `test_runner.py` script:

    $ python3 test_runner.py --help

`test_runner.py` script results will be similar to:


![test_framework_output](https://user-images.githubusercontent.com/11243503/63849665-11054400-c982-11e9-9156-08365da1de7f.png)

### Detailed about Test-Framework

To see information/examples about: framework, test writing or other utility objects: look <b>[section](docs/Framework.md)</b>.

### License

A copy of the license is available in the repository's
[LICENSE](LICENSE.txt) file.

