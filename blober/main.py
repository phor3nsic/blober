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

def permited(text):
    print(f'{RED}{text}{NC}')

# Ref: https://blog.intigriti.com/hacking-tools/hacking-misconfigured-aws-s3-buckets-a-complete-guide
def check_bucket_permissions(bucket_name, email=None):
    s3 = boto3.client('s3')

    permissions = {
        'list': False,
        'upload': False,
        'delete': False,
        'get_object': False,
        'get_bucket_acl': False,
        'get_object_acl': False,
        'put_bucket_acl': False,
        'put_object_acl': False,
        'get_bucket_versioning': False
    }

    # Test list permission
    try:
        s3.list_objects_v2(Bucket=bucket_name)
        permissions['list'] = True
        permited(f"[+] File list permitted to bucket {bucket_name}")
    except ClientError as e:
        print(f"[-] File list NOT permitted to bucket {bucket_name}: {e}")

    # Test upload permission
    try:
        s3.put_object(Bucket=bucket_name, Key='test_upload_file.txt', Body=b'This is a test file.')
        permissions['upload'] = True
        permited(f"[+] Upload permitted to bucket {bucket_name}")
        permited(f"[i] Open the link https://{bucket_name}.s3.amazonaws.com/test_upload_file.txt to see your file")
    except ClientError as e:
        print(f"[-] Upload NOT permitted to bucket {bucket_name}: {e}")

    # Test delete permission
    try:
        s3.delete_object(Bucket=bucket_name, Key='test_upload_file.txt')
        permissions['delete'] = True
        permited(f"[+] Remove file permitted to bucket {bucket_name}")
    except ClientError as e:
        print(f"[-] Remove file NOT permitted to bucket {bucket_name}: {e}")

    # Test get object permission (try to download 'index.html')
    try:
        s3.download_file(bucket_name, 'index.html', '/tmp/index.html')
        permissions['get_object'] = True
        permited(f"[+] Get object 'index.html' permitted from bucket {bucket_name}")
    except ClientError as e:
        print(f"[-] Get object 'index.html' NOT permitted from bucket {bucket_name}: {e}")

    # Test get bucket ACL
    try:
        acl = s3.get_bucket_acl(Bucket=bucket_name)
        permissions['get_bucket_acl'] = True
        permited(f"[+] Get bucket ACL permitted for bucket {bucket_name}")
        permited(f"ACL: {acl}")
    except ClientError as e:
        print(f"[-] Get bucket ACL NOT permitted for bucket {bucket_name}: {e}")

    # Test get object ACL (for 'index.html')
    try:
        acl = s3.get_object_acl(Bucket=bucket_name, Key='index.html')
        permissions['get_object_acl'] = True
        permited(f"[+] Get object ACL permitted for 'index.html' in bucket {bucket_name}")
        permited(f"ACL: {acl}")
    except ClientError as e:
        print(f"[-] Get object ACL NOT permitted for 'index.html' in bucket {bucket_name}: {e}")

    # Test put bucket ACL (grant full control to a specific email)
    if email:
        try:
            s3.put_bucket_acl(
                Bucket=bucket_name,
                GrantFullControl=f'emailaddress={email}'
            )
            permissions['put_bucket_acl'] = True
            permited(f"[+] Put bucket ACL permitted for bucket {bucket_name} (Granted full control to {email})")
        except ClientError as e:
            print(f"[-] Put bucket ACL NOT permitted for bucket {bucket_name}: {e}")
    
    if email:
        try:
            s3.put_object_acl(
                Bucket=bucket_name,
                GrantFullControl=f'emailaddress={email}',
                Key='index.html'
            )
            permissions['put_bucket_acl'] = True
            permited(f"[+] Put bucket ACL permitted for bucket {bucket_name} (Granted full control to {email})")
        except ClientError as e:
            print(f"[-] Put bucket ACL NOT permitted for bucket {bucket_name}: {e}")

    # Test get bucket versioning
    try:
        versioning = s3.get_bucket_versioning(Bucket=bucket_name)
        permissions['get_bucket_versioning'] = True
        permited(f"[+] Get bucket versioning permitted for bucket {bucket_name}")
        permited(f"Versioning: {versioning}")
    except ClientError as e:
        print(f"[-] Get bucket versioning NOT permitted for bucket {bucket_name}: {e}")

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
    parser.add_argument("-e", "--email", help="Email to try ACL permissions")
    args = parser.parse_args()

    if args.enviroment == "azure":
        check_blob_permissions(args.target)
        
    elif args.enviroment == "aws":
        bucket = args.target
        email = args.email
        check_bucket_permissions(bucket,email)

    elif args.enviroment == "google":
        bucket_name =args.target
        check_bucket_permissions(bucket_name)

    else:
        print("Invalid type. Use: aws/azure/google")


if __name__ == "__main__":
    main()