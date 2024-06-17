|Name|Type|Description|
|-|-|-|
|Rbs|list[float]|Blockade radii in units of the lattice spacing.|
|deltas|list[float]|Detuning from resonance.|
|betas|list[float]|Inverse temperatures.|
|Ls|list[int]|Linear system size, for a total number of atoms $N = L^2$.|
|interaction_graphs|list[object]|The interaction graphs for the corresponding parameters. Provided as a list of arrays where `array[i][j]` is the weight of the interaction between atom `i` and atom `j`.|
|samples|list[array]|Rydberg occupation measurements sampled from quantum Monte Carlo simulation. Given as $N_s × L × L$ binary arrays, where $N_s$ is the number of uncorrelated samples and is fixed at $N_s = 100000$.|
|energies|list[dict]|Energy values of the finite-size system computed from quantum Monte Carlo data. Provided as a list of dictionaries with keys: `mean`, `std` and `std_err`.|
|mags_stag|list[dict]|Staggered magnetization values of the finite-size system computed from quantum Monte Carlo data. Provided as a list of dictionaries with keys: `mean`, `std` and `std_err`.|
|mags_x|list[float]|X-magnetization values of the finite-size system computed from quantum Monte Carlo data. Provided as a list of mean magnetization values.|
