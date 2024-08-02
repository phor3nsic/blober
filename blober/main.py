from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient
import sys
import os

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
        
        print(f"[!] Upload of {file_path} to {blob_client.url} finish with success.")

    except Exception as e:
        print(f"[i] Error to upload files to blob: {e}")

def delete_blob(container_url, blob_name):
    try:
        # Extraia a parte do host e do contêiner da URL
        parsed_url = container_url.split('/')
        account_url = '/'.join(parsed_url[:3])
        container_name = parsed_url[3] if len(parsed_url) > 3 else ''
        
        if not container_name:
            raise ValueError("[i] Name of container not specified in url.")
        
        blob_service_client = BlobServiceClient(account_url=account_url)
        

        container_client = blob_service_client.get_container_client(container_name)
        

        blob_client = container_client.get_blob_client(blob_name)
        

        blob_client.delete_blob()
        
        print(f"Blob {blob_name} deleted of {container_url}.")

    except Exception as e:
        print(f"Error to delete blob: {e}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python blob_operations.py <operation> <container_url> [<blob_name> <file_path>]")
        print("operation: list, upload, delete")
        sys.exit(1)

    operation = sys.argv[1]
    container_url = sys.argv[2]

    if operation == "list":
        list_blob_urls(container_url)
    elif operation == "upload":
        if len(sys.argv) != 5:
            print("Usage: python blob_operations.py upload <container_url> <blob_name> <file_path>")
            sys.exit(1)
        blob_name = sys.argv[3]
        file_path = sys.argv[4]
        upload_blob(container_url, blob_name, file_path)
    elif operation == "delete":
        if len(sys.argv) != 4:
            print("Usage: python blob_operations.py delete <container_url> <blob_name>")
            sys.exit(1)
        blob_name = sys.argv[3]
        delete_blob(container_url, blob_name)
    else:
        print("Invalid Operation. Use: list, upload, delete")
        sys.exit(1)

if __name__ == "__main__":
    main()