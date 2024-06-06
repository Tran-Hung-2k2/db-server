import inspect

def check_config_keys(config):
    required_keys = ['POSTGRES_DBNAME', 'POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_HOST', 'POSTGRES_PORT', 'QUERY']
    
    for key in required_keys:
        if key not in config:
            return False
    return True

def get_string(config):
    code = inspect.cleandoc(f"""
from mage_ai.io.postgres import Postgres
from os import path

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_data_from_postgres(*args, **kwargs):
    config = {config}
    query = {config['QUERY']}
    with Postgres(
        dbname={config['POSTGRES_DBNAME']},
        user={config['POSTGRES_USER']},
        password={config['POSTGRES_PASSWORD']},
        host={config['POSTGRES_HOST']},
        port={config['POSTGRES_PORT']},
        schema=config.get('POSTGRES_SCHEMA'),
        connection_method=config.get('POSTGRES_CONNECTION_METHOD'),
        ssh_host=config.get('POSTGRES_SSH_HOST'),
        ssh_port=config.get('POSTGRES_SSH_PORT'),
        ssh_username=config.get('POSTGRES_SSH_USERNAME'),
        ssh_password=config.get('POSTGRES_SSH_PASSWORD'),
        ssh_pkey=config.get('POSTGRES_SSH_PKEY'),
        connect_timeout=config.get('POSTGRES_CONNECT_TIMEOUT')
    ) as loader:
        return loader.load(query)

@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
""")
    return code
