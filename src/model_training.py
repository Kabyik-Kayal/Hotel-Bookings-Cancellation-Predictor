import os
import pandas as pd
import joblib
import mlflow
import mlflow.sklearn
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import *
from utils.common_functions import read_yaml, load_data
from scipy.stats import uniform, randint

logger = get_logger(__name__)

class Model_Training:

    def __init__(self, train_path, test_path, model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path

        self.params_dist = LIGHTGBM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

    def load_and_split_data(self):
        try:
            logger.info(f"Loading Train data from {self.train_path}")
            train_df = load_data(self.train_path)

            logger.info(f"Loading Test data from {self.test_path}")
            test_df = load_data(self.test_path)

            X_train = train_df.drop(columns=['booking_status'])
            y_train = train_df['booking_status']
            X_test = test_df.drop(columns=['booking_status'])
            y_test = test_df['booking_status']
            logger.info("Data Splitted Successfully")

            return X_train, y_train, X_test, y_test
        
        except Exception as e:
            logger.error(f"Error in loading and splitting data: {e}")
            raise CustomException("Error while loading and splitting data",e)
        
    def train_model(self, X_train, y_train):
        try:
            logger.info("Initializing the model")
            model = lgb.LGBMClassifier(random_state=42, force_row_wise=True)
            
            logger.info("Starting hyperparameter tuning")
            
            random_search = RandomizedSearchCV(
                estimator=model,
                param_distributions=self.params_dist,
                n_iter=self.random_search_params['n_iter'],
                cv=self.random_search_params['cv'],
                n_jobs=self.random_search_params['n_jobs'],
                verbose=self.random_search_params['verbose'],
                scoring=self.random_search_params['scoring'],
            )
            random_search.fit(X_train, y_train)

            logger.info("Hyperparameter tuning completed")
            
            best_model = random_search.best_estimator_
            logger.info(f"Best Model Parameters are : {random_search.best_params_}")

            return best_model
        
        except Exception as e:
            logger.error(f"Error in training the model: {e}")
            raise CustomException("Error while training the model",e)
        
    def evaluate_model(self, model, X_test, y_test):
        try:
            logger.info("Evaluating the model")
            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)

            logger.info(f"Model Evaluation Metrics: Accuracy: {accuracy}, Precision: {precision}, Recall: {recall}, F1 Score: {f1}")

            return {"Accuracy" :accuracy, 
                    "Precision" :precision, 
                    "Recall" :recall,
                    "F1 Score" :f1}
        
        except Exception as e:
            logger.error(f"Error in evaluating the model: {e}")
            raise CustomException("Error while evaluating the model",e)
        
    def save_model(self, model):
        try:
            if not os.path.exists(os.path.dirname(self.model_output_path)):
                os.makedirs(os.path.dirname(self.model_output_path))
            logger.info(f"Saving the model to {self.model_output_path}")
            joblib.dump(model, self.model_output_path)
            logger.info("Model saved successfully")
        
        except Exception as e:
            logger.error(f"Error in saving the model: {e}")
            raise CustomException("Error while saving the model",e)
        
    def run(self):
        try:
            with mlflow.start_run():
                logger.info("Starting MLflow run")
                
                logger.info("Logging the training and testing dataset to MLflow")
                mlflow.log_artifact(self.train_path, artifact_path="datasets")
                mlflow.log_artifact(self.test_path, artifact_path="datasets")

                logger.info("Starting the model training process")
                X_train, y_train, X_test, y_test = self.load_and_split_data()
                model = self.train_model(X_train, y_train)
                metrics = self.evaluate_model(model, X_test, y_test)
                self.save_model(model)
                
                logger.info("Logging the model, parameters and metrics to MLflow")
                mlflow.log_artifact(self.model_output_path, artifact_path="models")
                mlflow.log_params(model.get_params())
                mlflow.log_metrics(metrics)

                logger.info("Model training process completed successfully")




        except Exception as e:
            logger.error(f"Error in the model training process: {e}")
            raise CustomException("Error in the model training process",e)
        
if __name__ == "__main__":
    trainer = Model_Training(
        train_path=PROCESSED_TRAIN_DATA_PATH,
        test_path=PROCESSED_TEST_DATA_PATH,
        model_output_path=MODEL_OUTPUT_PATH
    )
    trainer.run()