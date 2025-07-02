import os
import pandas as pd
import joblib 
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from src.logger import get_logger
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import LIGHTGBM_PARAMS, RANDOM_SEARCH_PARAMS
from utils.common_functions import load_data
import mlflow
import mlflow.sklearn


logger = get_logger(__name__)

class ModelTraining:
    def __init__(self,train_path,test_path,model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path

        self.params_dist = LIGHTGBM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS
    
    def load_and_split_data(self):
        try:
            logger.info("Loading training and testing data")
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            X_train = train_df.drop('booking_status', axis=1)
            y_train = train_df['booking_status']
            X_test = test_df.drop('booking_status', axis=1)
            y_test = test_df['booking_status']

            logger.info("Data loaded and split into features and booking_status")
            return X_train, y_train, X_test, y_test
        except Exception as e:
            logger.error(f"Error loading and splitting data: {e}")
            raise CustomException(f"Error loading and splitting data: {e}", e)

    
    def train_lgbm(self, X_train, y_train):
        try:
            logger.info("Initializing LightGBM model")
            model = lgb.LGBMClassifier(random_state=self.random_search_params['random_state'])
            
            logger.info("Hyperparameter tuning using RandomizedSearchCV")
            random_search = RandomizedSearchCV(estimator=model,
                                               param_distributions=self.params_dist,
                                               n_iter=self.random_search_params['n_iter'],
                                               cv=self.random_search_params['cv'],
                                               n_jobs=self.random_search_params['n_jobs'],
                                               verbose=self.random_search_params['verbose'],
                                               random_state=self.random_search_params['random_state'],
                                               scoring=self.random_search_params['scoring'])
            
            logger.info("Starting hyperparameter tuning")
            random_search.fit(X_train, y_train)
            logger.info("Hyperparameter tuning completed")
            best_params = random_search.best_params_
            best_lgbm_model = random_search.best_estimator_

            logger.info(f"Best parameters found: {best_params}")
            return best_lgbm_model
        except Exception as e:
            logger.error(f"Error during model training: {e}")
            raise CustomException(f"Error during model training: {e}", e)

    def evaluate_model(self, model, X_test, y_test):
        try:
            logger.info("Evaluating the model")

            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred, )
            recall = recall_score(y_test, y_pred, )
            precision = precision_score(y_test, y_pred,)

            logger.info(f"Model evaluation metrics - Accuracy: {accuracy}, F1 Score: {f1}, Recall: {recall}, Precision: {precision}")
            return {
                "accuracy": accuracy,
                "f1_score": f1,
                "recall": recall,
                "precision": precision
            }
        except Exception as e:
            logger.error(f"Error during model evaluation: {e}")
            raise CustomException(f"Error during model evaluation: {e}", e)
        
    
    def save_model(self, model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)
            joblib.dump(model, self.model_output_path)
            logger.info(f"Model saved to {self.model_output_path}")
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            raise CustomException(f"Error saving model: {e}", e)
        
    def run(self):
        try :
            with mlflow.start_run():
                logger.info("Starting model training process")

                logger.info("Starting MLFlow Experimentation")
                mlflow.log_artifact(self.train_path, artifact_path="datasets")
                mlflow.log_artifact(self.test_path, artifact_path="datasets")

                X_train, y_train, X_test, y_test = self.load_and_split_data()
                model = self.train_lgbm(X_train, y_train)
                evaluation_metrics = self.evaluate_model(model, X_test, y_test)
                self.save_model(model)

                logger.info("Logging model to MLFlow")
                mlflow.log_artifact(self.model_output_path)

                logger.info("Logging model parameters and metrics to MLFlow")
                mlflow.log_params(model.get_params())
                mlflow.log_metrics(evaluation_metrics)


                logger.info("Model training process completed successfully")
                return evaluation_metrics
        except Exception as e:
            logger.error(f"Error in model training process: {e}")
            raise CustomException(f"Error in model training process: {e}", e)
        

if __name__ == "__main__":
    try:
        model_training = ModelTraining(PROCESSED_TRAIN_DATA_PATH,PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH)
        evaluation_metrics = model_training.run()
        logger.info(f"Model training completed with metrics: {evaluation_metrics}")
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        raise CustomException(f"Error in main execution: {e}", e)