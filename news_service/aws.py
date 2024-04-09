import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION")


class S3_Manager:
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )

    def upload_image(self, file, bucket_name, filename):
        try:
            folder = "post_images/"
            key = folder + filename
            self.s3.upload_fileobj(file, bucket_name, key)
            return f"https://{bucket_name}.s3.{AWS_REGION}.amazonaws.com/{key}"
        except ClientError as e:
            print("Error uploading file to S3:", e)
            return None


s3_manager = S3_Manager(AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION)
