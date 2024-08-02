import sys
import os
import argparse
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient

# COLOURS
RED='\033[0;31m'
WHITE='\033[0;37m'
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

    # Teste de upload de arquivo
    try:
        s3.put_object(Bucket=bucket_name, Key='test_upload_file.txt', Body=b'This is a test file.')
        permissions['upload'] = True
        print(f"[+] {RED} Upload permited to bucket {bucket_name} {NC}")
    except ClientError as e:
        print(f"[-] Upload NOT permited to bucket {bucket_name}: {e}")

    # Teste de remoção de arquivo
    try:
        s3.delete_object(Bucket=bucket_name, Key='test_upload_file.txt')
        permissions['delete'] = True
        print(f"[+] {RED}Remove file permited to bucket {bucket_name}{NC}")
    except ClientError as e:
        print(f"[-] Remove file NOT permited to bucket {bucket_name}: {e}")

    return permissions

def list_blob_urls(container_url):
    try:
        parsed_url = container_url.split('/')
        account_url = '/'.join(parsed_url[:3])
        container_name = parsed_url[3] if len(parsed_url) > 3 else ''
        
        if not container_name:
            raise ValueError("[i] Name of container not specified in url.")

        blob_service_client = BlobServiceClient(account_url=account_url)
        
        container_client = blob_service_client.get_container_client(container_name)
        
        blob_list = container_client.list_blobs()

        for blob in blob_list:
            blob_url = f"{container_url}/{blob.name}"
            print(blob_url)

    except Exception as e:
        print(f"[-] Error to list blobs: {e}")

def upload_blob(container_url, blob_name, file_path):
    try:
        parsed_url = container_url.split('/')
        account_url = '/'.join(parsed_url[:3])
        container_name = parsed_url[3] if len(parsed_url) > 3 else ''
        
        if not container_name:
            raise ValueError("[i] Name of container not specified in url.")
        
        # Conecte-se ao serviço de blobs
        blob_service_client = BlobServiceClient(account_url=account_url)
        
        # Obtenha o cliente do contêiner
        container_client = blob_service_client.get_container_client(container_name)
        
        # Obtenha o cliente do blob
        blob_client = container_client.get_blob_client(blob_name)
        
        # Faça upload do arquivo
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        
        print(f"[!] {RED}Upload of {file_path} to {blob_client.url} finish with success.{NC}")

    except Exception as e:
        print(f"[i] Error to upload files to blob: {e}")

def delete_blob(container_url, blob_name):
    try:
        parsed_url = container_url.split('/')
        account_url = '/'.join(parsed_url[:3])
        container_name = parsed_url[3] if len(parsed_url) > 3 else ''
        
        if not container_name:
            raise ValueError("[i] Name of container not specified in url.")
        
        blob_service_client = BlobServiceClient(account_url=account_url)
        

        container_client = blob_service_client.get_container_client(container_name)
        

        blob_client = container_client.get_blob_client(blob_name)
        

        blob_client.delete_blob()
        
        print(f"[+] {RED}Blob {blob_name} deleted of {container_url}.{NC}")

    except Exception as e:
        print(f"[i] Error to delete blob: {e}")

def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("enviroment", help="Enviroment to test: aws/azure")
    parser.add_argument("-op","--operation", help="Operations to azure test: list,upload,delete")
    parser.add_argument("-t", "--target", help="Target to check, EX: AWS - only name of bucket / AZURE - url of container", required=True)
    parser.add_argument("-n", "--blob_name", help="Name of blob (only for azure)")
    parser.add_argument("-f","--file", help="File to upload")
    args = parser.parse_args()

    

    if args.enviroment == "azure":
        operation = args.operation
        container_url = args.target
        if operation == "list":
            list_blob_urls(container_url)
        elif operation == "upload":
            blob_name = args.blob_name
            file_path = args.file
            upload_blob(container_url, blob_name, file_path)
        elif operation == "delete":
            blob_name = args.blob_name
            delete_blob(container_url, blob_name)
        else:
            print("Invalid Operation. Use: list, upload, delete")
            sys.exit(1)
    elif args.enviroment == "aws":
        bucket = args.target
        check_bucket_permissions(bucket)

    else:
        print("Invalid type. Use: aws or azure")


if __name__ == "__main__":
    main()