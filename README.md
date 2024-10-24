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

## Adding new dataset content

For datasets to appear on [pennylane.ai/datasets](https://pennylane.ai/datasets), a `dataset.json` file describing it must
be added to the [content/](content) directory. This can be done using the `dsets add dataset.h5` command, which will derive some details
of the dataset from its `.h5` file.

Run the `dsets add` command. You will be prompted for the class slug of the dataset, i.e `qchem`, `qspin`, `other`. A class
slug corresponds to the name of the directories directly under `content`.

```bash
(.venv) pennylane-datasets $ dsets add Max3Sat_Max3Sat.h5
Class slug: other
```

If the class slug does not exist, you will be prompted for details of the class, including title and parameter info. Attribute
information will be automatically generated from the `.h5` file. All details should be verified by checking the generated
`class.json` file.

```bash
(.venv) pennylane-datasets $ dsets add H2_STO-3G_0.742.h5
Class slug: qchem
Enter class name [Qchem]: Qchem
Define parameters for class 'qchem'? [Y/n]: Y
Enter parameter name (leave blank to finish): molname
        Enter title for parameter 'molname' [Molname]: 
        Enter description for parameter 'molname': Molecule name
Enter parameter name (leave blank to finish): basis
        Enter title for parameter 'basis' [Basis]: 
        Enter description for parameter 'Basis': Molecular basis
Enter parameter name (leave blank to finish): bondlength
        Enter title for parameter 'bondlength' [Bondlength]: Bondlength
        Enter description for parameter 'bondlength': Bond length
Enter parameter name (leave blank to finish): molname 
Created class file: content/qchem/_meta/class.json
```

You will then be prompted for the dataset family slug. This slug corresponds to the directory under the class directory that contains the
`dataset.json` file. If no `dataset.json` file exists with the slug, you will be prompted for details of the dataset family:

```bash
Created class file: content/qchem/_meta/class.json
Enter family slug [h2-molecule]: 
Creating new family with slug 'h2-molecule'
Enter title [H2 Molecule]: 
Enter download name [name]: molname
Enter authors (author1,author2,...): Adam A, Alex B
Wrote data to content/qchem/h2-molecule/dataset.json
```

This will automatically generate several metadata files in the family directory, including the `meta.json`, `using_this_dataset.md` and a `citation.txt`
file containing the BibTex citation for the dataset. `using_this_dataset.md` should be completed with a description of the dataset and all files should be verified and manually adjusted before committing.

## Building

After adding new content, test the build by running:

```bash
(.venv) pennylane-datasets $ dsets build
Created build: file=PosixPath('_build/datasets-build.json')
```

This will compile all content into a single file in `_build/datasets-build.json`, and copy any referenced
assets (e.g images) to `_build/assets`.

To deploy the build, open a pull request on https://github.com/XanaduAI/pennylane-datasets.

## Login

To login to your `pennylane.ai` account via the CLI, please run the following command:
 ```bash
(.venv) pennylane-datasets $ dsets login
Checking credentials...
```

This will run a check that searches for a valid authorization token on your local machine. If this is the first time using 
the CLI login function, or if an existing token has expired, the login flow will be triggered. This will direct you to a  `pennylane.ai` login webpage in your browser. In this window you can enter your associated email and password. If successful
the corresponding CLI output will look like:

```bash
Checking credentials...
No valid credentials found.
Starting login to 'https://xanadu-swc.us.auth0.com/oauth'
User code is 'ABCD-EFGH'
Go to 'https://xanadu-swc.us.auth0.com/activate' to complete authentication.
Successfully saved new token.
You are logged into your pennylane.ai account.
```

where a new token has been saved to your machine. Alternatively, if you already have a valid token on your machine, the login
flow will not be triggered and the CLI output will look like:

```bash
Checking credentials...
Found a valid token
You are logged into your pennylane.ai account.
```
