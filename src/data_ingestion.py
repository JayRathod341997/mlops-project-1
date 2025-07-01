import os
import pandas as pd
from google.cloud import storage
from src.logger import get_logger
from src.custom_exception import CustomException 
from config.paths_config import RAW_DIR, RAW_FILE_PATH, TRAIN_FILE_PATH, TEST_FILE_PATH, CONFIG_PATH
# from config.paths_config import * 
from utils.common_functions import read_yaml

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, config: str):
        self.config = config['data_ingestion']
        self.bucket_name = self.config['bucket_name']
        self.file_name= self.config['bucket_file_name']
        self.train_test_ratio = self.config['train_ratio']

        os.makedirs(RAW_DIR, exist_ok=True)
        logger.info(f"Data Ingestion initialized with bucket: {self.bucket_name}, file: {self.file_name}, train-test ratio: {self.train_test_ratio}")

    def download_csv_from_gcp(self):
        try:
            # Initialize the Google Cloud Storage client
            self.storage_client = storage.Client()
            bucket = self.storage_client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)

            # Download the file to the local path
           
            blob.download_to_filename(RAW_FILE_PATH)
            logger.info(f"File downloaded from GCP bucket {self.bucket_name} to {RAW_FILE_PATH}")
        except Exception as e:
            logger.error(f"Error downloading file from GCP: {e}")
            raise CustomException(f"Error downloading file from GCP: {e}",e)

    def split_data(self):
        try:
            logger.info(f"Splitting data into train and test sets with ratio {self.train_test_ratio}")
            df = pd.read_csv(RAW_FILE_PATH)
            train_df = df.sample(frac=self.train_test_ratio, random_state=42)
            test_df = df.drop(train_df.index)

            train_df.to_csv(TRAIN_FILE_PATH, index=False)
            test_df.to_csv(TEST_FILE_PATH, index=False)

            logger.info(f"Data split into train and test sets")
        except Exception as e:
            logger.error(f"Error splitting data: {e}")
            raise CustomException(f"Error splitting data: {e}",e)
        
    def run(self):
        try:
            self.download_csv_from_gcp()
            self.split_data()
        except Exception as e:
            logger.error(f"Error occurred during data ingestion: {e}")
            raise CustomException(f"Error occurred during data ingestion: {e}",e)

if __name__ == "__main__":
    data_ingestion_config = read_yaml(CONFIG_PATH)
    data_ingestion = DataIngestion(data_ingestion_config)
    data_ingestion.run()