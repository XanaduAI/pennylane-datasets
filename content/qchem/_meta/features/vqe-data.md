Variational data obtained by using [`AdaptiveOptimizer`](https://docs.pennylane.ai/en/stable/code/api/pennylane.AdaptiveOptimizer.html#pennylane.AdaptiveOptimizer) to minimize ground state energy.

> **Warning**: This data is not available for this dataset. It only exists for datasets with up to 20 spin orbitals.

| Name            | Type              | Description                                                    |
|-----------------|-------------------|----------------------------------------------------------------|
| `vqe_gates`     | list[[`Operation`](https://docs.pennylane.ai/en/stable/code/api/pennylane.operation.Operation.html#pennylane.operation.Operation)] | [`SingleExcitation`](https://docs.pennylane.ai/en/stable/code/api/pennylane.SingleExcitation.html#pennylane.SingleExcitation) and [`DoubleExcitation`](https://docs.pennylane.ai/en/stable/code/api/pennylane.DoubleExcitation.html#pennylane.DoubleExcitation) gates for the optimized circuit                   |
| `vqe_params`     | `numpy.ndarray` | Optimal parameters for the gates that prepares ground state                   |
| `vqe_energy`     | `float` | Energy obtained from the state prepared by the optimized circuit                   |