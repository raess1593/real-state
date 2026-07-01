import logging

import pandas as pd

logger = logging.getLogger(__name__)


class DataTransformer:
    def __init__(self, json_file_path: str):
        self.file_path = json_file_path
        self.df = None

    def load_data(self) -> None:
        try:
            self.df = pd.read_json(self.file_path)
            logger.info(f"Data loaded successfully. Shape: {self.df.shape}")
        except Exception as e:
            logger.error(f"Failed to load JSON data: {e}")
            raise

    def clean_prices(self) -> None:
        try:
            self.df["price"] = (
                self.df["price"].str.replace(r"[^\d]", "", regex=True).str.strip()
            )

            self.df["price"] = self.df["price"].fillna("0")
            self.df["price"] = self.df["price"].astype(int)
            logger.info("Prices cleaned successfully.")
        except Exception as e:
            logger.error(f"Error occurred while cleaning prices: {e}")
            raise

    def clean_meters(self) -> None:
        try:
            self.df["meters"] = (
                self.df["meters"].str.replace(r"[^\d]", "", regex=True).str.strip()
            )
            self.df["meters"] = self.df["meters"].fillna("0")
            self.df["meters"] = self.df["meters"].astype(int)
            logger.info("Meters cleaned successfully.")
        except Exception as e:
            logger.error(f"Error occurred while cleaning meters: {e}")
            raise

    def fill_missing_text(self) -> None:
        try:
            for column in ["title", "location"]:
                self.df[column] = self.df[column].fillna("Unknown")
            logger.info("Missing text fields filled successfully.")
        except Exception as e:
            logger.error(f"Error occurred while filling missing text fields: {e}")
            raise

    def run_pipeline(self) -> pd.DataFrame:
        self.load_data()
        self.clean_prices()
        self.clean_meters()
        self.fill_missing_text()
        return self.df
