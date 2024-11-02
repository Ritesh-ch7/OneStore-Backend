import boto3
import botocore
from fastapi import HTTPException
from fastapi.responses import StreamingResponse


s3 = boto3.client("s3")
BUCKET_NAME = "lambdatestbucketritesh"  # Replace with your S3 bucket name

def upload_file(file_name, file_content):
    try:
        s3.upload_fileobj(file_content, BUCKET_NAME, file_name)
    except botocore.exceptions.ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))

def download_file(file_name):
    try:
        # Create a temporary file path
        temp_file_path = f"/tmp/{file_name}"  # Ensure this directory is writable

        # Download the file from S3 to a temporary file
        s3.download_file(BUCKET_NAME, file_name, temp_file_path)

        # Return the file as a streaming response
        return StreamingResponse(open(temp_file_path, "rb"),
                                 media_type='application/octet-stream',
                                 headers={"Content-Disposition": f"attachment; filename={file_name}"})
    except botocore.exceptions.ClientError as e:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_s3_file_count():
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)
    return len(response["Contents"]) if "Contents" in response else 0
