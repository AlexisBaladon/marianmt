import os

from src.model import model
from src.components import data_ingestion
from src.config.ingestion_config import DataIngestionConfig
from src.config.command_config import CommandConfig
from src.config.data_transformation_config import DataTransformationConfig
from src.config.hyperparameter_tuning_config import HyperparameterTuningConfig
from src.components import hyperparameter_tuning

TEMP_DIR = 'temp.txt'

def get_hyperparameter_flags(default_flags, hyperparameter_grids, hyperparameter_configs, search_method):
    # type: (list[str], list[list[dict]], list[dict], str) -> list[dict]
    hyperparameter_grids_flags = []
    for hyperparameter_grid in hyperparameter_grids:
        hyperparameter_grids_flags.extend(hyperparameter_tuning.get_grid_flags(default_flags, hyperparameter_grid))
    hyperparameter_configs_flags = [hyperparameter_tuning.get_custom_config_flags(default_flags, hyperparamter_config) for hyperparamter_config in hyperparameter_configs]
    trained_flags = [*hyperparameter_configs_flags, *hyperparameter_grids_flags]
    return trained_flags

def save_checkpoint(temp_file, checkpoint):
    with open(temp_file, 'w') as f:
        f.write(checkpoint)

def load_checkpoint(temp_file):
    checkpoint = 0
    if os.path.isfile(temp_file):
        with open(temp_file, 'r') as f:
            checkpoint = int(f.read())
    return checkpoint

def delete_checkpoint(temp_file):
    os.remove(temp_file)

def train(
    data_ingestion_config,
    data_transformation_config,
    command_config,
    hyperparameter_tuning_config,
):
    # type: (DataIngestionConfig, DataTransformationConfig, CommandConfig, HyperparameterTuningConfig) -> None
    default_flags = command_config.flags
    trained_flags = [default_flags]

    if hyperparameter_tuning_config is not None:
        hyperparamter_grids, hyperparameter_configs, hyperparameter_method = \
            hyperparameter_tuning_config.tuning_grid_files, hyperparameter_tuning_config.tuning_params_files, \
            hyperparameter_tuning_config.search_method
        trained_flags = get_hyperparameter_flags(default_flags, hyperparamter_grids, hyperparameter_configs, hyperparameter_method)

    loaded_checkpoint = load_checkpoint(TEMP_DIR)
    for idx, current_flags in enumerate(trained_flags[loaded_checkpoint:]):
        save_checkpoint(TEMP_DIR, str(idx))

        if data_ingestion_config:
            data_ingestion.ingest_data(data_ingestion_config)

        if data_transformation_config:
            pass

        if command_config:
            command_config.flags = current_flags
            model.train(command_config)

    delete_checkpoint(TEMP_DIR)