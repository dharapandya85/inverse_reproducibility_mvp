import pypdf
from utils.logger import setup_logger
logger=setup_logger(__name__)
class PDFExtractor:
    def __init__(self,pdf_path):
        self.pdf_path=pdf_path
    def extract_text(self):
        text=" "
        try:
            with open(self.pdf_path,'rb') as f:
                reader=pypdf.PDFReader(f)
                for page_num in range(len(reader.pages)):
                    page=reader.pages[page_num]
                    text+=page.extract_text() or ""
            logger.info(f"Successfully extracted text from {len(reader.pages)} pages of {self.pdf_path}")
        except Exception as e:
            logger.error(f'Error extracting text from PDF {self.pdf_path}:{e}')
            raise
        return text

