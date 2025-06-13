import os # Make sure to import os at the top of the file if not already there
from utils.logger import setup_logger # Assuming logger is correctly imported

logger = setup_logger(__name__)

class TextExtractor:
    def __init__(self, manuscript_path):
        self.manuscript_path = manuscript_path
        # logger = setup_logger(__name__) # Initialize logger here if needed, or globally in module

    def extract_text(self):
        if not os.path.exists(self.manuscript_path):
            logger.error(f"Text file not found: {self.manuscript_path}")
            raise FileNotFoundError(f"Text file not found: {self.manuscript_path}")

        try:
            with open(self.manuscript_path, 'r', encoding='utf-8') as file:
                text = file.read()
            logger.info(f"Successfully extracted content from text file: {self.manuscript_path}")
            return text
        except Exception as e:
            logger.error(f"Error extracting text from text file {self.manuscript_path}:{e}")
            raise