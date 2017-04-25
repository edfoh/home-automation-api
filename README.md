# home-automation-api

API that sends signals to television via IP to change channels, input sources and power off.

### Prerequisites

- Python 2.7 ([here](https://www.python.org/download/releases/2.7/) OR [via homebrew](https://brew.sh/))
- pip ([here](https://pip.pypa.io/en/stable/installing/) OR [via homebrew](https://brew.sh/))
- `pip install pip-tools` [pip-tools](https://github.com/nvie/pip-tools)
- `pip install virtualenv` [virtualenv](https://virtualenv.pypa.io/en/stable/)

### VirtualEnv and install dependencies

    virtualenv myenv
    source myenv/bin/activate
    pip install pip-tools
    ./install.sh

#### Add a python lib

1. Add it to the [requirements.in](requirements.in) file
1. Run `./install.sh`

#### Remove a python lib

1. Run `rm -rf lib`
1. Remove it from the [requirements.in](requirements.in) file
1. Run `./install.sh`

### Running locally

- run `./src/app.py`
