import os
import pandas as pd
import json
from .data_loader import DataLoader
from .data_transformer import DataTransformer
from utils.logger import setup_logger

logger=setup_logger(__name__)
class DataProcessor:
    def __init__(self,dataset_paths,output_dir):
        self.dataset_paths=dataset_paths
        self.output_dir=os.path.join(output_dir,"data","processed")
        os.makedirs(self.output_dir, exist_ok=True)
        self.loaded_data = {}
        self.processed_data_paths = []

    def process_data(self, processing_instructions=None):
        if processing_instructions is None:
            processing_instructions = {}

        data_loader = DataLoader()
        data_transformer = DataTransformer()

        for dataset_path in self.dataset_paths:
            logger.info(f"Loading dataset: {dataset_path}")
            data_id = os.path.basename(dataset_path).split('.')[0]
            try:
                loaded_df = data_loader.load_data(dataset_path)
                self.loaded_data[data_id] = loaded_df

                logger.info(f"Applying processing instructions for {data_id}...")
                processed_df = data_transformer.transform_data(loaded_df, processing_instructions.get(data_id, {}))

                processed_file_path = os.path.join(self.output_dir, f"{data_id}_processed.csv")
                processed_df.to_csv(processed_file_path, index=False)
                self.processed_data_paths.append(processed_file_path)
                logger.info(f"Processed data saved to: {processed_file_path}")

            except Exception as e:
                logger.error(f"Failed to process dataset {dataset_path}: {e}")
                # Decide whether to raise or just log and continue
                raise

        return self.processed_data_paths