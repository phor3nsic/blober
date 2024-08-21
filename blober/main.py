import sys
import os
import argparse
import boto3
import requests

from google.cloud import storage
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from google.api_core.exceptions import Forbidden, NotFound


# COLOURS
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

def check_bucket_permissions(bucket_name):
    s3 = boto3.client('s3')

    permissions = {
        'list': False,
        'upload': False,
        'delete': False
    }

    try:
        s3.list_objects_v2(Bucket=bucket_name)
        permissions['list'] = True
        print(f"[+] {RED}File list permited to bucket {bucket_name}{NC}")
    except ClientError as e:
        print(f"[-] File list NOT permited to bucket {bucket_name}: {e}")

    try:
        s3.put_object(Bucket=bucket_name, Key='test_upload_file.txt', Body=b'This is a test file.')
        permissions['upload'] = True
        print(f"[+] {RED} Upload permited to bucket {bucket_name} {NC}")
        print(f"[i] Open the link {GREEN}https://{bucket_name}.s3.amazonaws.com/test_upload_file.txt{NC} to see your file")
    except ClientError as e:
        print(f"[-] Upload NOT permited to bucket {bucket_name}: {e}")

    try:
        s3.delete_object(Bucket=bucket_name, Key='test_upload_file.txt')
        permissions['delete'] = True
        print(f"[+] {RED}Remove file permited to bucket {bucket_name}{NC}")
    except ClientError as e:
        print(f"[-] Remove file NOT permited to bucket {bucket_name}: {e}")

    return permissions

def check_blob_permissions(container_url):
    permissions = {
        'list': False
    }

    try:
        # https://{name}.blob.core.windows.net/{containername}
        list_url = f"{container_url}?restype=container&comp=list"
        
        # Teste de listagem de blobs no container
        list_response = requests.get(list_url)
        if list_response.status_code == 200:
            permissions['list'] = True
            print(f"[+] {RED}Listing blobs is permitted for container at {GREEN}{container_url} {NC}")
        else:
            print(f"[-] Listing blobs is NOT permitted for container at {container_url}: HTTP {list_response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

    return permissions

def check_google_bucket_permissions(bucket_name):
    permissions = {
        'list': False,
        'upload': False,
        'delete': False
    }

    try:
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)

        # Test listing objects
        try:
            blobs = list(bucket.list_blobs())
            permissions['list'] = True
            print(f"[+] {RED}Listing objects permitted for bucket {GREEN}{bucket_name}{NC}")
        except Forbidden as e:
            print(f"[-] Listing objects NOT permitted for bucket {bucket_name}: {e}")

        # Test uploading an object
        try:
            blob = bucket.blob('test_upload_file.txt')
            blob.upload_from_string('This is a test file.')
            permissions['upload'] = True
            print(f"[+] {RED}Upload permitted to bucket {GREEN}{bucket_name}{NC}")
            print(f"[i] Open the link to see your file: {GREEN}https://storage.googleapis.com/{bucket_name}/test_upload_file.txt{NC}")
        except Forbidden as e:
            print(f"[-] Upload NOT permitted to bucket {bucket_name}: {e}")

        # Test deleting the object
        try:
            blob.delete()
            permissions['delete'] = True
            print(f"[+] Deleting objects permitted for bucket {bucket_name}")
        except (Forbidden, NotFound) as e:
            print(f"[-] Deleting objects NOT permitted for bucket {bucket_name}: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")

    return permissions

def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("enviroment", help="Enviroment to test: aws/azure/google")
    parser.add_argument("-t", "--target", help="Target to check, EX: AWS/GOOGLE - only name of bucket / AZURE - url of container ", required=True)
    args = parser.parse_args()

    if args.enviroment == "azure":
        check_blob_permissions(args.target)
        
    elif args.enviroment == "aws":
        bucket = args.target
        check_bucket_permissions(bucket)

    elif args.enviroment == "google":
        bucket_name =args.target
        check_bucket_permissions(bucket_name)

    else:
        print("Invalid type. Use: aws/azure/google")


if __name__ == "__main__":
    main()