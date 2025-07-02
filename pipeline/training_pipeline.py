from utils.common_functions import read_yaml
from config.paths_config import *
from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataPreprocessor
from src.model_training import ModelTraining

if __name__=='__main__':
    #### 1. Data Ingestion
    # data_ingestion_config = read_yaml(CONFIG_PATH)
    # data_ingestion = DataIngestion(data_ingestion_config)
    # data_ingestion.run()

    #### 2. Data Preprocessing
    data_preprocessor = DataPreprocessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    data_preprocessor.process()

    #### 3. Model Training
    model_training = ModelTraining(PROCESSED_TRAIN_DATA_PATH,PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH)
    evaluation_metrics = model_training.run()