import pandas as pd
from utils.logger import setup_logger
logger=setup_logger(__name__)
class DiffAnalyzer:
    def compare_images(self,image_path1,image_path2,threshold=0.9):
        logger.warning(f"Image comparison is a placeholder")
        return True
    def compare_tables(self,df1,df2,tolerance=1e-6):
        if not isinstance(df1,pd.DataFrame) or not isinstance(df2,pd.DataFrame):
            logger.warning('Table comparison requires pandas DataFrames.')
            return False
        if not df1.equals(df2):
            if df1.shape!=df2.shape:
                logger.debug(f"Table shapes differ:{df1.shape} vs {df2.shape}")
                return False
            if not df1.columns.equals(df2.columns):
                logger.debug(f"Table colmuns differ:{df1.columns.tolist()} vs {df2.columns.tolist()}")
                return False
            diff=(df1-df2).abs()
            if(diff>tolerance).any().any():
                logger.debug(f"Numerical differences found beyond tolerance.")
                return False
            non_numeric_cols=df1.select_dtypes(exclude=['number']).columns
            if not df1[non_numeric_cols].equals(df2[non_numeric_cols]):
                logger.debug(f"Non-numerical differences found.")
                return False
        return True

                        