import boto3
import os

def copy_to_s3(bucket_name, source_directory):
    s3 = boto3.client('s3')
    
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            local_path = os.path.join(root, file)
            s3_path = os.path.relpath(local_path, source_directory)
            s3_key = os.path.join(bucket_name, s3_path)
            s3.upload_file(local_path, bucket_name, s3_key)
            print(f"Uploaded '{local_path}' to S3 bucket '{bucket_name}' as '{s3_key}'")

def validate_s3_files(bucket_name, source_directory):
    s3 = boto3.client('s3')
    
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            local_path = os.path.join(root, file)
            s3_path = os.path.relpath(local_path, source_directory)
            s3_key = os.path.join(bucket_name, s3_path)
            
            try:
                s3.head_object(Bucket=bucket_name, Key=s3_key)
                print(f"File '{local_path}' is successfully copied to S3 bucket '{bucket_name}' as '{s3_key}'")
            except Exception as e:
                print(f"Error: File '{local_path}' is not copied to S3 bucket '{bucket_name}'. Reason: {str(e)}")

# Replace with your AWS credentials and region
aws_access_key_id = 'YOUR_ACCESS_KEY'
aws_secret_access_key = 'YOUR_SECRET_ACCESS_KEY'
aws_region = 'us-west-2'

# Replace with your EC2 instance details
ec2_instance_ip = 'EC2_INSTANCE_IP'
ec2_key_pair = 'EC2_KEY_PAIR_NAME'
ec2_username = 'EC2_USERNAME'
source_directory = '/path/to/source/directory'

# Replace with your S3 bucket details
s3_bucket_name = 'YOUR_S3_BUCKET_NAME'

# Connect to the EC2 instance
ec2_client = boto3.client('ec2', region_name=aws_region,
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key)

# Generate the SSH command to copy files from EC2 instance to local directory
ssh_command = f"scp -i {ec2_key_pair}.pem -r {ec2_username}@{ec2_instance_ip}:{source_directory} ."

# Copy files from EC2 instance to local directory
os.system(ssh_command)

# Upload files from local directory to S3 bucket
copy_to_s3(s3_bucket_name, source_directory)

# Validate if files are copied to S3 bucket
validate_s3_files(s3_bucket_name, source_directory)
