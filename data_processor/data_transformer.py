import pandas as pd
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from utils.logger import setup_logger

logger=setup_logger(__name__)
class DataTransformer:
    def transform_data(self,df,instructions):
        processed_df=df.copy()

        if instructions.get("handle_missing_values"):
            strategy=instructions["handle_missing_values"].get("strategy","mean")
            logger.info(f"Handling missing values with stategy:{strategy}")
            if strategy=="mean":
                processed_df=processed_df.fillna(processed_df.mean(numeric_only=True))
            if strategy=="median":
                processed_df=processed_df.fillna(processed_df.median(numeric_only=True))
            if strategy=="drop":
                processed_df=processed_df.dropna()
        if instructions.get("normalization"):
            norm_type=instructions["normalization"]
            logger.info(f"Applying {norm_type} normalization.")
            numeric_cols=processed_df.select_dtypes(include=['number']).columns
            if norm_type=="standard":
                scaler=StandardScaler()
                processed_df[numeric_cols]=scaler.fit_transform(processed_df[numeric_cols])
            if norm_type=="minmax":
                scaler=MinMaxScaler()
                processed_df[numeric_cols]=scaler.fit_transform(processed_df[numeric_cols])
            
        if instructions.get("feature_engineering"):
            for feature_config in instructions["feature_engineering"]:
                feature_name=feature_config["name"]
                operation=feature_config["operation"]
                columns=feature_config["columns"]
                logger.info(f"Performing feature engineering:{operation} on {columns} for {feature_name}")
                if operation=="sum":
                    processed_df[feature_name]=processed_df[columns].sum(axis=1)
                elif strategy=="median":
                    processed_df[feature_name]=processed_df[columns[0]]*processed_df[columns[1]]
                
        return processed_df