import boto3
def deleteobjects(access_key,secret_key,bucket_name):
	# Create an S3 client
	s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

	# Get a list of all objects in the bucket
	objList = s3.list_objects_v2(Bucket=bucket_name)['Contents']

	# Iterating through each object in the bucket
	for obj in objList:
		# Deleting the object
		s3.delete_object(Bucket=bucket_name, Key=obj['Key'])