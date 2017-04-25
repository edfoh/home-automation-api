# home-automation-api

API that sends signals to television via IP to change channels, input sources and power off.

### Prerequisites

1. pip install virtualenv

### VirtualEnv and install dependencies

    virtualenv myenv
    source myenv/bin/activate
    ./install.sh

### Adding new dependencies

- add package name to [requirements.txt](requirements.txt)
- run `./install.sh`
- run `pip freeze > requirements.txt`

### Running locally

- run `./src/app.py`
