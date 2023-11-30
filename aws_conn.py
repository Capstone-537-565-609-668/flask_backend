import boto3
import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()


s3 = boto3.client(
    service_name='s3',
    region_name='us-east-2',
    aws_access_key_id=os.getenv("AWS_S3_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_S3_SECRET_ACCESS_KEY")
)
my_bucket = "spatialpolygon"


def uploadFolder(local_folder_path, dataset_id, bucket_name=my_bucket, s3_client=s3):
    print(local_folder_path)
    for root, dirs, files in os.walk(local_folder_path):
        for file in files:
            local_file_path = os.path.join(root, file)
            s3_file_path = os.path.relpath(local_file_path, local_folder_path)
            s3_key = os.path.join('outputs', f"{dataset_id}", s3_file_path)
            with open(local_file_path, 'rb') as data:
                s3_client.put_object(
                    Bucket=bucket_name, Key="/".join(s3_key.split("\\")), Body=data)
