import logging
import boto3
import os
from botocore.exceptions import ClientError
def uploadfileToCloud(access_key,secret_key,bucket_name):
    # Creating an S3 client
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    localPath='./encrypted/'
    for file in os.listdir(localPath):
        file_path = os.path.join(localPath, file)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f1:
                object_key = file
                s3.upload_fileobj(f1, bucket_name, object_key)
