# blober

Script to test blobs permitions

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
Usage: blober <operation> <container_url> [<blob_name> <file_path>]
operation: list, upload, delete
```

Example:

```sh
blober list https://myblob.blob.core.windows.net/example
```