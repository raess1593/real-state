from scraper import RealEstateScraper
from cloud_manager import AWSCloudManager
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    bucket_name = os.getenv("AWS_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("AWS_BUCKET_NAME is not set in the environment variables")

    scraper = RealEstateScraper(page_limit=5)   
    output_file = scraper.run()

    manager = AWSCloudManager(bucket_name=bucket_name)
    manager.upload_json(output_file)