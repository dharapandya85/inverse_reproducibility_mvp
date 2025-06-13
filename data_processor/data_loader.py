# inverse_reproducibility/data_processor/data_loader.py

import pandas as pd
import json
from utils.logger import setup_logger

logger = setup_logger(__name__)

class DataLoader:
    def load_data(self, file_path):
        file_extension = file_path.split('.')[-1].lower()
        if file_extension == 'csv':
            logger.debug(f"Loading CSV: {file_path}")
            return pd.read_csv(file_path)
        elif file_extension == 'json':
            logger.debug(f"Loading JSON: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Attempt to flatten JSON if it's not directly tabular
            try:
                return pd.json_normalize(data)
            except Exception as e:
                logger.warning(f"Could not directly normalize JSON to DataFrame, returning raw data: {e}")
                return data # Return raw JSON if it can't be normalized to a simple DataFrame
        # Add support for other data formats like Excel, SQL database dumps etc.
        else:
            raise ValueError(f"Unsupported data file type: {file_extension} for {file_path}")