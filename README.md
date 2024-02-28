# Pennylane Datasets

Repository for managing Pennylane Dataset HDF5 files and metadata for the datasets
service.

## Organization

- The [data/](data/) directory contains 'upload reciepts' representing data files uploaded
to the data bucket.
- The [lib/](lib/) directory contains the command line app for managing datasets

# Usage

## Installation

The `dsets` app requires Python 3.11. It is recommened to install in a virtual
environment:

```bash
pennylane-datasets $ python3.11 -m venv .venv
pennylane-datasets $ source .venv/bin/activate
(.venv) pennylane-datasets $ pip install .
```

## Uploading a Dataset

Dataset HDF5 files can be uploaded with the `dsets upload` command. This requires write access to
the `swc-prod-pennylane-datasets` bucket in the Software Cloud production account. If you
need credentials, contact the Software Cloud team.

The S3 key of the uploaded file will be in the form: `data/{filename}/{upload_timestamp}-{file_sha1_hash}`

For example, the dataset file `H2_STO-3G_0.742.h5`, uploaded on midnight, will have the key:

`data/H2_STO-3G_0.742.h5/2024-01-01T000000Z-e98e34a7d58e039da35f793cb6d9bd0da78847f9`

This ensures that data files are uniquely identified by their content, as well as sorted
by upload date.

The upload will create a 'receipt' file in the [data/](data) directory, in the same path
as the file was uploaded. These are used to track the contents of the data bucket with
git, so create a new branch before uploading:

```bash
(.venv) pennylane-datasets $ git checkout -b upload-max3sat
```

Then run `dsets upload` command:

```bash
(.venv) pennylane-datasets $ dsets upload Max3Sat_Max3Sat.h5
Uploading 'Max3Sat_Max3Sat.h5'
Generating SHA1 hash.. ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.2 GB   1.2 GB/s 0:00:04
Uploading...           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.2 GB 11.0 MB/s 0:09:36
File uploaded to 'data/Max3Sat_Max3Sat.h5/2024-02-27T155839Z-4a06dbb748c8ae32cf6f15b18833c467e4bb2a3b'. Be sure to commit upload receipt!
```
