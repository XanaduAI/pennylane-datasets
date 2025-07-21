Basic descriptors of the molecule.

| Name            | Type       | Description                                                                 |
|-----------------|------------|-----------------------------------------------------------------------------|
| `name`          | `string`   | Full name of the molecule.                                                 |
| `mf`            | `string`   | Molecular formula of the compound.                                         |
| `cid`           | `int`    | PubChem Compound ID (CID) for the molecule.                                |
| `spin`          | `int`      | Total spin number of the molecule.                                 |
| `multiplicity`  | `int`      | Spin multiplicity of the molecule (M = 2S+1).                                  |
| `charge`        | `int`      | Electric charge of the molecule.
| `basis`         | `string`   | Basis set used for the quantum chemistry calculations.                     |
| `bond_length`   | `float`    | Specific bond length set from the coordinates in Angstroms.         |
| `symbols`       | `list[str]`| List of atomic symbols (e.g., H, C, N, O) corresponding to each atom.      |
| `coordinates`   | `list[list[float]]` | List of 3D Cartesian coordinates (x, y, z) for each atom.      |