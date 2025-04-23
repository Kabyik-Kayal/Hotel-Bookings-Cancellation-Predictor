import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml, load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)

class DataProcessor:

    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)
        
    def preprocess_data(self, df):
        try:
            logger.info("started data preprocessing step")

            logger.info("Dropping unnecessary columns")
            df.drop(columns=["Unnamed: 0","Booking_ID"], inplace=True)
            df.drop_duplicates(inplace=True)

            cat_cols = self.config['data_processing']['categorical_columns']
            num_cols = self.config['data_processing']['numerical_columns']

            logger.info("Label Encoding categorical columns")

            label_encoder = LabelEncoder()

            mappings = {}

            for col in cat_cols:
                df[col] = label_encoder.fit_transform(df[col])
                mappings[col] = {label:code for label, code in zip(label_encoder.classes_ , label_encoder.transform(label_encoder.classes_))}
            
            logger.info("Label Mappings are : ")
            for col, mapping in mappings.items():
                logger.info(f"{col}: {mapping}")

            logger.info("Handling Skewness of Data")
            
            skewness_threshold = self.config['data_processing']['skewness_threshold']
            skewness = df[num_cols].apply(lambda x: x.skew())
            for column in skewness[skewness > skewness_threshold].index:
                df[column] = np.log1p(df[column])
            
            return df

        except Exception as e:
            logger.error(f"Error in data preprocessing {e}")
            raise CustomException("Error in data preprocessing", e)
    
    def handle_imbalance(self, df):
        try:
            logger.info("Handling Imbalance in Data")
            X = df.drop(columns=["booking_status"])
            y = df["booking_status"]

            smote = SMOTE(random_state=42)
            X_resampled, y_resampled = smote.fit_resample(X, y)

            balanced_df = pd.DataFrame(X_resampled, columns=X.columns)
            balanced_df["booking_status"] = y_resampled

            logger.info("Data balanced successfully")

            return balanced_df
        
        except Exception as e:
            logger.error(f"Error in handling imbalance {e}")
            raise CustomException("Error in handling imbalance", e)
        
    def select_features(self, df):
        try:
            logger.info("Feature Engineering started")
            X = df.drop(columns=["booking_status"])
            y = df["booking_status"]

            model = RandomForestClassifier(random_state=42)
            model.fit(X, y)

            feature_importance = model.feature_importances_
            feature_importance_df = pd.DataFrame({
                "Feature": X.columns,
                "Importance": feature_importance
            })
            top_important_features_df = feature_importance_df.sort_values(by="Importance", ascending=False)
            
            num_features_to_select = self.config['data_processing']['num_of_features']
            top_features = top_important_features_df["Feature"].head(num_features_to_select).values
            
            logger.info(f"Top {num_features_to_select} features selected: {top_features}")
            
            top_df = df[top_features.tolist() + ["booking_status"]]

            logger.info("Feature Engineering completed successfully")
            
            return top_df
        
        except Exception as e:
            logger.error(f"Error in feature engineering {e}")
            raise CustomException("Error in feature engineering", e)
    
    def save_processed_data(self, df, file_path):
        try:
            logger.info(f"Saving data in {file_path}")
            df.to_csv(file_path, index=False)
            logger.info("Data saved successfully")

        except Exception as e:
            logger.error(f"Error in saving data {e}")
            raise CustomException("Error while saving data", e)
        
    def process_data(self):
        try:
            logger.info("Loading data from RAW directory")

            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)

            train_df = self.handle_imbalance(train_df)
            test_df = self.handle_imbalance(test_df)

            train_df = self.select_features(train_df)
            test_df = test_df[train_df.columns]

            self.save_processed_data(train_df, PROCESSED_TRAIN_DATA_PATH)
            self.save_processed_data(test_df, PROCESSED_TEST_DATA_PATH)

            logger.info("Data processing completed successfully")

        except Exception as e:
            logger.error(f"Error in data processing {e}")
            raise CustomException("Error in data processing", e)
        

if __name__ == "__main__":
    processor = DataProcessor(
        train_path=TRAIN_FILE_PATH,
        test_path=TEST_FILE_PATH,
        processed_dir=PROCESSED_DIR,
        config_path=CONFIG_PATH
    )
    processor.process_data()