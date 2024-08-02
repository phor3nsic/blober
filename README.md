# blober

Script to test AZURE blober and AWS buckets permitions

### Install

- via pipx:

```sh
pipx install git+https://github.com/phor3nsic/blober
```
- via pip:

```sh
pip install git+https://github.com/phor3nsic/blober
```
### Usage:

Help

```sh
usage: blober [-h] [-op OPERATION] -t TARGET [-n BLOB_NAME] [-f FILE] enviroment

positional arguments:
  enviroment            Enviroment to test: aws/azure

options:
  -h, --help            show this help message and exit
  -op OPERATION, --operation OPERATION
                        Operations to azure test: list,upload,delete
  -t TARGET, --target TARGET
                        Target to check, EX: AWS - only name of bucket / AZURE - url of container
  -n BLOB_NAME, --blob_name BLOB_NAME
                        Name of blob (only for azure)
  -f FILE, --file FILE  File to upload
```

Example list in azure blober:

```sh
blober azure -op list -t https://myblob.blob.core.windows.net/example
```

Example to check aws bucket:

```sh
blober aws -t mybucket
```