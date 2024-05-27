|Name|Type|Description|
|-|-|-|
|Rbs|list[float]|Blockade radii in units of the lattice spacing.|
|deltas|list[float]|Detuning from resonance.|
|betas|list[float]|Inverse temperatures.|
|Ls|list[int]|Linear system size, for a total number of atoms $N = L^2$.|
|interaction_graphs|list[object]|The interaction graphs for the corresponding parameters.|
|samples|list[array]|The QMC samples as a $N_s × L × L$ binary array, where $N_s$ is the number of uncorrelated samples and is fixed at $N_s = 100000$.|
|observables|list[dict]|Observable values of the finite-size system computed from QMC data. The observables include energy, x-magnetization, and staggered magnetization, as well as the associated variances and standard errors.|
