import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv 



load_dotenv()

BUCKET_NAME = "fast-api-testing"
REGION = os.getenv("REGION")


s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=REGION
)

def upload_to_s3(file):
     
    try:

        # Upload file
        s3_path = f"laiba/{file.filename}"
 
        s3.upload_fileobj(
            file.file,
            BUCKET_NAME,
            s3_path
            
        )
        file_url=f"https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/{s3_path}"

        return  file_url

    except Exception as e:
        print("Error uploading to S3:", str(e))
    
