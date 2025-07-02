import os
import pandas
from src.logger import get_logger
from src.custom_exception import CustomException
import yaml

logger = get_logger(__name__)

def read_yaml(file_path: str) -> dict:
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"YAML file not found at {file_path}")
        with open(file_path, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
            logger.info(f"YAML file read successfully from {file_path}")
            return config
    except Exception as e:
        logger.error(f"Error reading YAML file at {file_path}: {e}")
        raise CustomException(f"Error reading YAML file: {e}",e)

def load_data(path):
    try:
        data = pandas.read_csv(path)
        logger.info(f"Data loaded successfully from {path}")
        return data
    except Exception as e:
        logger.error(f"Error loading data from {path}: {e}")
        raise CustomException(f"Error loading data: {e}",e) 
    

