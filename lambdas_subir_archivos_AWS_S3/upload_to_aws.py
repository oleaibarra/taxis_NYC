import boto3
import os
import requests
from botocore.exceptions import NoCredentialsError

def upload_to_aws(download_url, s3_file):
    s3 = boto3.client('s3')

    try:
        response = requests.get(download_url)
        if response.status_code != 200:
            print("Error downloading the file")
            return None

        s3.upload_fileobj(response.raw, os.environ['BUCKET_NAME'], s3_file)
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': os.environ['BUCKET_NAME'],
                'Key': s3_file
            },
            ExpiresIn=24 * 3600
        )

        print("Upload Successful", url)
        return url
    except FileNotFoundError:
        print("The file was not found")
        return None
    except NoCredentialsError:
        print("Credentials not available")
        return None
