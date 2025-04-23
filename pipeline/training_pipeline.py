from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataProcessor
from src.model_training import Model_Training
from utils.common_functions import read_yaml
from config.paths_config import *

if __name__ == "__main__":

    # 1. Data Ingestion
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run_data_ingestion_and_splitting()

    # 2. Data Preprocessing
    processor = DataProcessor(
        train_path=TRAIN_FILE_PATH,
        test_path=TEST_FILE_PATH,
        processed_dir=PROCESSED_DIR,
        config_path=CONFIG_PATH
    )
    processor.process_data()

    # 3. Model Training
    trainer = Model_Training(
        train_path=PROCESSED_TRAIN_DATA_PATH,
        test_path=PROCESSED_TEST_DATA_PATH,
        model_output_path=MODEL_OUTPUT_PATH
    )
    trainer.run()