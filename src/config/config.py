import os
import json

MODEL_NAME = 'MODEL_NAME'
COMMAND_NAME = 'COMMAND_NAME'
FLAG_SEPARATOR = 'FLAG_SEPARATOR'
BASE_DIR_SCRIPTS = 'BASE_DIR_SCRIPTS'
BASE_DIR_ARTIFACTS = 'BASE_DIR_ARTIFACTS'
TEST_SRC_CORPUS_FILENAME = 'TEST_SRC_CORPUS_FILENAME'
TEST_DST_CORPUS_FILENAME = 'TEST_DST_CORPUS_FILENAME'
RAW_DATA_FILENAME = 'RAW_DATA_FILENAME'
RAW_DATA_COLUMNS_TO_CLEAN = 'RAW_DATA_COLUMNS_TO_CLEAN'
RAW_DATA_SPLIT_COLUMN = 'RAW_DATA_SPLIT_COLUMN'
RAW_DATA_TRAIN_COLUMN = 'RAW_DATA_TRAIN_COLUMN'
RAW_DATA_VALIDATION_COLUMN = 'RAW_DATA_VALIDATION_COLUMN'
RAW_DATA_TEST_COLUMN = 'RAW_DATA_TEST_COLUMN'

CONFIG_VARIABLES = [
    MODEL_NAME,
    COMMAND_NAME,
    FLAG_SEPARATOR,
    BASE_DIR_SCRIPTS,
    BASE_DIR_ARTIFACTS,
    TEST_SRC_CORPUS_FILENAME,
    TEST_DST_CORPUS_FILENAME,
    RAW_DATA_FILENAME,
    RAW_DATA_COLUMNS_TO_CLEAN,
    RAW_DATA_SPLIT_COLUMN,
    RAW_DATA_TRAIN_COLUMN,
    RAW_DATA_VALIDATION_COLUMN,
    RAW_DATA_TEST_COLUMN,
]

def load_config_variables():
    # type: () -> dict
    root_abs_dir = os.path.join(os.path.dirname(__file__), '..', '..')
    config_variables_path = os.path.join(root_abs_dir, 'config.json')

    config_variables = {}
    with open(config_variables_path, 'r') as config_variables_file:
        config_variables = json.load(config_variables_file)

    variable_names = CONFIG_VARIABLES
    config_variables = {
        variable_name: config_variables[variable_name.lower()] 
        for variable_name in variable_names
    }

    return config_variables