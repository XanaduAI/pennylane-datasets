from pathlib import Path
import json

for dataset_json_path in Path("content/qchem/").rglob("*/dataset.json"):
    with open(dataset_json_path, "rb") as f:
        data = json.load(f)

    ## Do something
    
    with open(dataset_json_path, "w") as f:
        json.dump(
            data, f, indent=2
        )

