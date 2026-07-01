import logging
import os

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class AWSCloudManager:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client("s3")

    def upload_json(self, file_path: str, object_name: str = None) -> bool:
        if not object_name:
            object_name = os.path.basename(file_path)

        try:
            self.s3_client.upload_file(
                Filename=file_path, Bucket=self.bucket_name, Key=object_name
            )
            logger.info(f"Successfully uploaded {file_path} to S3")
            return True

        except ClientError as e:
            logger.error(f"Failed to upload {file_path} to S3: {e}")
            return False

    def download_latest_json(
        self, prefix: str = "data", local_path: str = "latest_data.json"
    ) -> bool:
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name, Prefix=prefix
            )
            if "Contents" not in response:
                logger.warning(
                    f"No objects found in bucket {self.bucket_name} with prefix {prefix}"
                )
                return False

            latest_object = max(
                response["Contents"], key=lambda obj: obj["LastModified"]
            )
            self.s3_client.download_file(
                Bucket=self.bucket_name, Key=latest_object["Key"], Filename=local_path
            )
            logger.info(
                f"Successfully downloaded the latest JSON from S3 to {local_path}"
            )
            return True

        except ClientError as e:
            logger.error(f"Failed to download the latest JSON from S3: {e}")
            return False
