import inspect

def check_config_keys(config):
    required_keys = ['COLUMNS', 'STRATEGY']
    
    for key in required_keys:
        if key not in config:
            return False
    if config['STRATEGY'] not in {'average', 'column', 'constant', 'median', 'mode', 'no_action', 'random', 'remove_rows', 'sequential'}:
        return False
    return True

def get_string(config):
    code = inspect.cleandoc(f"""
from mage_ai.data_cleaner.transformer_actions.constants import ImputationStrategy
from mage_ai.data_cleaner.transformer_actions.base import BaseAction
from mage_ai.data_cleaner.transformer_actions.constants import ActionType, Axis
from mage_ai.data_cleaner.transformer_actions.utils import build_transformer_action
from pandas import DataFrame

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def execute_transformer_action(df: DataFrame, *args, **kwargs) -> DataFrame:
    action = build_transformer_action(
        df,
        action_type=ActionType.IMPUTE,
        arguments={config['COLUMNS']}, 
        axis=Axis.COLUMN,
        options={'strategy': {config['STRATEGY']}},
    )

    return BaseAction(action).execute(df)

@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
    """)
    return code
