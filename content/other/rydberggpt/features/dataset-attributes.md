|Name|Type|Description|
|-|-|-|
|Rbs|list|Blockade radii in units of the lattice spacing.|
|deltas|list[int]|Number of gates used in the circuits above.|
|betas|list[int]|Inverse temperatures.|
|Ls|list[int]|Linear system size, for a total number of atoms $N = L^2$.|
|ineraction_graphs|list[int]|Linear system size, for a total number of atoms $N = L^2$.|
|samples|list[int]|The QMC samples as a $N_s × L × L$ binary array, where $N_s$ is the number of uncorrelated samples and is fixed at $N_s = 100000$ for all parameter points.|
|observables|list[int]|Linear system size, for a total number of atoms $N = L^2$.|
