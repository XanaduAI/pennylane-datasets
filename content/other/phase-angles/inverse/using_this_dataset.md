This dataset contains phase angles that can be used to approximate the function 1/x via [Quantum Signal Processing (QSP)](https://pennylane.ai/qml/demos/function_fitting_qsp) and [Quantum Singular Value Transformation (QSVT)](https://pennylane.ai/qml/demos/tutorial_intro_qsvt), making it easy to implement polynomial transformations without additional calculations.

**Description of the dataset**

QSVT and QSP can be used to implement polynomial transformations in quantum algorithms. This dataset provides phase angles to implement QSVT and QSP for an approximation of the inverse, $1/x$.

More specifically, we approximate  $f(x) = \frac{1}{2\kappa x}$ with a [Chebyshev polynomial](https://en.wikipedia.org/wiki/Chebyshev_polynomials), $P(x)$. The values $\kappa$ and $\epsilon$ define the approximation:
- **Kappa** is a scaling factor in $f(x)$ and determines in which interval the function is approximated.
- **Epsilon** represents the maximum error allowed in the polynomial approximation: $\max_{x}|P(x)-f(x)|$

**Additional Details**

* The Chebysev polynomial $P(x)$ approximates the function $f(x) = \frac{1}{2\kappa x}$ over the interval $[-1, -1/\kappa) \cup (1/\kappa, 1]$ with a maximum error of $\epsilon$. 
* $\kappa$ can take values from the set $\{1, 5, 50, 100, 250, 500, 1000, 1500\}$, and its choice depends on the specific interval in which we aim to approximate the function. 
* The Chebyshev polynomial, $P(x)$ can be accessed via `dataset.poly[epsilon][kappa]`. This returns an array where, for example, $[1, 0, 2]$ corresponds to the polynomial $ 1 \cdot T_0(x) + 0 \cdot T_1(x) + 2 \cdot T_2(x) $, where $T_n(x)$ denotes the $n$-th Chebyshev polynomial. These can be easily implemented using [NumPy's Chebyshev polynomial class](https://numpy.org/doc/stable/reference/generated/numpy.polynomial.chebyshev.Chebyshev.html#).
* Phase angles to implement these Chebyshev polynomials via QSP (or QSVT) can be accessed using  `dataset.angles[routine][epsilon][kappa]`
* This dataset was generated using numerical optimization techniques to find optimal phase angles that minimize the error in the polynomial approximation.

**Graphical Representation**

The following figure illustrates the polynomial approximation of $ f(x) = \frac{1}{2\kappa x} $ with $ \kappa = 250 $ and $ \epsilon = 0.01 $:

<p style="text-align: center"><img src="https://assets.cloud.pennylane.ai/datasets/generic/using_this_dataset/phase-angles-inverse.png" alt="drawing" width="70%"/></p>

The blue line represents the polynomial approximation, the orange dashed line corresponds to $f(x)$, and the red dashed lines show $x = \pm 1/\kappa$. 

**Example usage**

The following example shows how to plot the output of the qsvt algorithm and compare to the original Chebyshev approximation.

```python
import pennylane as qml
import numpy as np
import matplotlib.pyplot as plt

[dataset] = qml.data.load("other", name="inverse")
angles_qsvt = dataset.angles["qsvt"]["0.01"]["100"] 

outputs_qsvt = []
points = np.arange(-1, 1, 1/300)

for x in points:

    # Encode x in the top left of the matrix
    block_encoding = qml.RX(2 * np.arccos(x), wires=0)
    projectors = [qml.PCPhase(angle, dim=1, wires=0) for angle in angles_qsvt]

    @qml.qnode(qml.device("default.qubit"))
    def circuit_qsvt():
        qml.QSVT(block_encoding, projectors)
        return qml.state()

    output = qml.matrix(circuit_qsvt, wire_order=[0])()[0, 0]

    outputs_qsvt.append(output.real)

poly = np.polynomial.Chebyshev(dataset.poly['0.01']['100'])
outputs_poly = [poly(point) for point in points]

plt.plot(points, outputs_qsvt, '.')
plt.plot(points, outputs_poly)
plt.show()
```