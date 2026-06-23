import os
import logging
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class AWSCloudManager:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3')

    def upload_json(self, file_path: str, object_name: str = None) -> bool:
        if object_name is None:
            object_name = os.path.basename(file_path)

        try:
            self.s3_client.upload_file(
                Filename=file_path,
                Bucket=self.bucket_name,
                Key=object_name
            )
            return True
        
        except ClientError as e:
            logger.error(f"Failed to upload {file_path} to S3: {e}")
            return False