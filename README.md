<h1 align="center">blober</h1>

<h4 align="center">Test public permissions on AWS S3, Azure Blob Storage and Google Cloud Storage buckets</h4>

<p align="center">
  <a href="#about">About</a> •
  <a href="#install">Install</a> •
  <a href="#usage">Usage</a> •
  <a href="#license">License</a>
</p>

<p align="center">
  <img alt="language" src="https://img.shields.io/github/languages/top/phor3nsic/blober">
  <img alt="last commit" src="https://img.shields.io/github/last-commit/phor3nsic/blober">
  <img alt="license" src="https://img.shields.io/github/license/phor3nsic/blober">
  <img alt="stars" src="https://img.shields.io/github/stars/phor3nsic/blober?style=social">
</p>

## About

`blober` checks cloud storage buckets for misconfigured permissions. Given a target,
it probes which operations are publicly allowed so you can spot exposed or
over-permissive buckets during recon.

It supports three providers:

- **AWS S3** — tests list, upload, delete, get-object, bucket/object ACL read, ACL write (with `-e`) and versioning.
- **Azure Blob Storage** — tests anonymous blob listing on a container.
- **Google Cloud Storage** — tests list, upload and delete.

## Install

```bash
# via pipx
pipx install git+https://github.com/phor3nsic/blober

# via pip
pip install git+https://github.com/phor3nsic/blober
```

> AWS and Google checks use the cloud SDKs (`boto3`, `google-cloud-storage`),
> so they rely on whatever credentials are configured in your environment.

## Usage

```bash
blober <environment> -t <target> [-e EMAIL]
```

| Flag | Description | Default |
|------|-------------|---------|
| `environment` | Provider to test: `aws`, `azure` or `google` | — |
| `-t`, `--target` | Target to check. AWS/Google: bucket name. Azure: container URL | — |
| `-e`, `--email` | Email used when testing S3 ACL-write permissions | — |
| `-h`, `--help` | Show help and exit | — |

## Examples

```bash
# Check an AWS S3 bucket
blober aws -t mybucket

# Test S3 ACL-write by granting full control to an email
blober aws -t mybucket -e you@example.com

# List blobs in an Azure container
blober azure -t https://myblob.blob.core.windows.net/example

# Check a Google Cloud Storage bucket
blober google -t mybucket
```

## Disclaimer

For authorized security testing and education only. You are responsible for how you use it.

## License

[MIT](LICENSE) © [phor3nsic](https://github.com/phor3nsic)
