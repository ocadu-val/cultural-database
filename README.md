# Cultural Database tooling
This repo contains tools for migrating data from csv files to sqlite and
scripts for running data analysis.

## Setup
You will need to install [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation) or python.
After installing pyenv. Run the following commands to install the correct python version.
```bash
pyenv install $(cat .python-version)
```

Create a virtual environment
```bash
python -m venv .env
```

Activate the virtual environment
```bash
source .env/bin/activate
```

Install the dependencies
```bash
pip install -r requirements.txt
```

## Running the scripts
With the virtual env active run the script:
### Create database
Run this command once the first time to create the database
```bash
python -m src.create_db
```

### Migrate data
Run this command to migrate the data from csv to the database engine
```bash
python -m src.migrate_data
```
