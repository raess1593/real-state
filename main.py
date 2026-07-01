import os

from dotenv import load_dotenv

from cloud_manager import AWSCloudManager
from scraper import RealEstateScraper

load_dotenv()

if __name__ == "__main__":
    bucket_name = os.getenv("AWS_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("AWS_BUCKET_NAME is not set in the environment variables")

    scraper = RealEstateScraper(page_limit=5)
    output_file = scraper.run()
    file_name = os.path.basename(output_file)

    s3_folder = "data"
    s3_object_name = f"{s3_folder}/{file_name}"

    manager = AWSCloudManager(bucket_name=bucket_name)
    manager.upload_json(output_file, object_name=s3_object_name)
