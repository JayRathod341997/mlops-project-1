import os
import numpy as np
import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException
from utils.common_functions import load_data, read_yaml
from config.paths_config import *

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)

class DataPreprocessor:
    def __init__(self, train_path,test_path, processed_dir ,config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)
            logger.info(f"Created directory: {self.processed_dir}")
    
    def preprocess_data(self,df):
        try:
            logger.info("Starting data preprocessing...")

            logger.info("Dropping the columns")
            df.drop(columns=['Booking_ID'] , inplace=True)
            df.drop_duplicates(inplace=True)

            cat_cols = self.config['data_processing']['categorical_features']
            num_cols = self.config['data_processing']['numerical_features']

            label_encoder = LabelEncoder()
            mappings={}

            for col in cat_cols:
                df[col] = label_encoder.fit_transform(df[col])
                mappings[col] = {label:code for label,code in zip(label_encoder.classes_ , label_encoder.transform(label_encoder.classes_))}
                
            logger.info("Label Mapping:")
            for col, mapping in mappings.items():
                logger.info(f"{col}: {mapping}")
            
            logger.info("Doing skewness treatment")
            skew_threshold = self.config['data_processing']['skew_threshold']
            skewness = df[num_cols].apply(lambda x: x.skew())
            for column in skewness[skewness > skew_threshold].index:
                df[column] = np.log1p(df[column])
            logger.info("Skewness treatment done")
            
            return df 
        except Exception as e:
            logger.error(f"Error during data preprocessing: {e}")
            raise CustomException(f"Error during data preprocessing: {e}",e) 
    
    def balance_data(self,df):
        try:
            logger.info("Starting data balancing...")

            X = df.drop(columns=['booking_status'])
            y = df['booking_status']

            smote = SMOTE(random_state=42)
            X_resampled, y_resampled = smote.fit_resample(X, y)

            balanced_df = pd.DataFrame(X_resampled, columns=X.columns)
            balanced_df['booking_status'] = y_resampled

            logger.info("Data balancing completed successfully.")
            return balanced_df
        except Exception as e:
            logger.error(f"Error during data balancing: {e}")
            raise CustomException(f"Error during data balancing: {e}",e)
        
    def select_features(self,df):
        try:
            logger.info("Starting feature selection...")

            X = df.drop(columns=['booking_status'])
            y = df['booking_status']

            model = RandomForestClassifier(random_state=42)
            model.fit(X, y)
            feature_importance = model.feature_importances_
            feature_importance_df = pd.DataFrame({
                                'feature':X.columns,
                                'importance':feature_importance
                            })
            top_features_importance_df = feature_importance_df.sort_values(by="importance" , ascending=False)
            no_of_features_to_select = self.config['data_processing']['no_of_features_to_select']
            
            top_10_features = top_features_importance_df["feature"].head(no_of_features_to_select).values

            logger.info(f"Top {no_of_features_to_select} features selected: {top_10_features.tolist()}")

            top_10_df = df[top_10_features.tolist() + ["booking_status"]]

            logger.info("Feature selection completed successfully.")
            return top_10_df

        except Exception as e:
            logger.error(f"Error during feature selection: {e}")
            raise CustomException(f"Error during feature selection: {e}",e)
        

    def save_data(self,df,file_path):
        try:
            logger.info(f"Saving data to {file_path}...")
            df.to_csv(file_path, index=False)
            logger.info(f"Data saved successfully to {file_path}")
        except Exception as e:
            logger.error(f"Error saving data to {file_path}: {e}")
            raise CustomException(f"Error saving data: {e}",e)
        
    
    def process(self):
        try:
            logger.info("Starting data processing pipeline...")

            train_data = load_data(self.train_path)
            test_data = load_data(self.test_path)

            train_data = self.preprocess_data(train_data)
            test_data = self.preprocess_data(test_data)

            train_data = self.balance_data(train_data)
            test_data = self.balance_data(test_data)

            train_data = self.select_features(train_data)
            test_data = test_data[train_data.columns.tolist()]  # Ensure test data has the same columns as train data

            self.save_data(train_data, PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_data, PROCESSED_TEST_DATA_PATH)

            logger.info("Data processing pipeline completed successfully.")
        except Exception as e:
            logger.error(f"Error in data processing pipeline: {e}")
            raise CustomException(f"Error in data processing pipeline: {e}",e)
    

if __name__ == "__main__":
    
    data_preprocessor = DataPreprocessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    data_preprocessor.process()