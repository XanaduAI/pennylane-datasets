from pathlib import Path
import json


def camel_case(string):
   words = string.split('-')
   camel_case_string = words[0].lower() + ''.join(word.title() for word in words[1:])
   return camel_case_string[:1].upper() + camel_case_string[1:]

for dataset_json_path in Path("content/qchem/").rglob("*/dataset.json"):
    with open(dataset_json_path, "rb") as f:
        data = json.load(f)

    s3_url = "https://datasets.cloud.pennylane.ai/datasets/h5"

    ### QChem
    molecule = data['downloadName']

    for block in data['data']:
        basis = block['parameters']['basis']
        bond_len = block['parameters']['bond_length']

        filename = molecule + "_" + basis + "_" + bond_len + ".h5"
        data_url = s3_url + "/qchem/" + molecule + "/" + basis + "/" + bond_len + "/" + filename

        block["dataUrl"] = data_url

    # ### Other

    # ds_name = camel_case(data["downloadName"])
    # filename = ds_name + "_" + ds_name + ".h5"
    # data_url =  s3_url + "/other/" + ds_name + "/" + filename
    
    # data['data'][0]["dataUrl"] = data_url

    with open(dataset_json_path, "w") as f:
        json.dump(
            data, f, indent=2
        )
