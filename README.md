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

### Detailed about Test-Framework

To see information/examples about: framework, test writing or other utility objects: look <b>[section](docs/Framework.md)</b>.
