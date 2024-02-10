# JobJourney Backend

[[_TOC_]]

## Contributing

For contributing/setting up this project please read [CONTRIBUTING.md](../CONTRIBUTING.md).

## Service Dependencies On MacOS

### Setting up homebrew

Homebrew is a CLI that provides easy package management in macOS (and Linux)
[Installation](https://brew.sh/) is pretty straight forward:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Docker

Isolated container does wonders to spin up self-contained execution environments for databases by mimicking server
setups without polluting development space, Docker can be installed directly
from [docker.io](https://docs.docker.com/desktop/mac/install/) as a _.dmg_ or via brew cask `brew install --cask docker`
. Note that going through brew installation requires the setup to be completed by running docker in Applications and
going through the GUI to install helper tools.

### Install required libraries

```bash
brew install poetry postgresql postgis jq
```

### Setup PostgreSQL database

You will need to have a postgres DB running with the right configurations on your local machine.

* You can either download a Postgres server or run a local DB using docker. For amd64 arch you can run:

```bash
docker run --restart unless-stopped --name job_journey_postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:16.1
```

* After having the local DB running, you can configure the right user permissions and database with this:

```bash
export PGPASSWORD=password
cat ./scripts/postgres_init.sql | psql -h localhost -U postgres -d postgres
```

### Setup redis

* Run a local standalone redis with the following command:

```bash
docker run --restart unless-stopped --name secure_redis -p 127.0.0.1:6379:6379 -d redis:alpine
```

### Setup rabbitmq

* Run a local standalone rabbitmq service with the following command:

```bash
docker run --restart unless-stopped --name secure_rabbitmq -e RABBITMQ_DEFAULT_USER=job_journey -e RABBITMQ_DEFAULT_PASS=password -p 127.0.0.1:15672:15672 -p 127.0.0.1:5672:5672 -d rabbitmq:3.11-management
```

## Local Development

### Install python versions manager

* Install `pyenv` to manage multiple python versions. Follow on-screen instructions and restart your shell.

```bash
curl https://pyenv.run | bash
```

Add pyenv to .zshrc or .bashrc by running the following commands (replace .zshrc to .bashrc depending on shell)

```
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -)"\nfi' >> ~/.zshrc
source ~/.zshrc
```

```bash
export PYTHON_VER=3.12.1
pyenv install ${PYTHON_VER}
```

*Note*: you might need readline and openssl libraries to be installed with brew before if not installed already.

* Set your global python version with pyenv

```bash
pyenv global ${PYTHON_VER}
```

* Create a new virtual environment with pyenv and set it to be used locally

```bash
pyenv virtualenv job_journey_venv
pyenv local job_journey_venv
```

### Installing poetry package dependency manager

This project uses [Poetry](https://python-poetry.org/) as a Package/Dependency Manager. You can see the installation
alternatives [here](https://python-poetry.org/docs/#installation). Once you have it installed execute the installation
command to setup the Python environment:

* Install poetry

```bash
curl -sSL https://install.python-poetry.org | python -
```

* Add Poetry to your PATH

The installer creates a poetry wrapper in a well-known, platform-specific directory:

```
$HOME/.local/bin on Unix.
%APPDATA%\Python\Scripts on Windows.
$POETRY_HOME/bin if $POETRY_HOME is set.
```

Add the following to your shell:

```bash
export PATH="${PATH}:${HOME}/.local/bin"
```

### Install application dependencies

* Create a virtual environment and install python requirements

```bash
poetry export --only=main --output requirements.txt --without-hashes && pip install --no-cache-dir -r requirements.txt
```

### Add environment file

* Get an env file that has development keys.

```bash
cp .env-template .env
cp .env-template-compose .env-compose
```

The `.env-template` already has the values needed for development purposes.


### Initialize the database for the first time

```bash
python manage.py migrate
```


### Run the django development server for the API component

```bash
python manage.py runserver
```
