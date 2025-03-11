|Name|Type|Description|
|-|-|-|
|angles|dict|Angles that apply the polynomial transformation for a given routine. This is provided as a dictionary of lists with form `angles[routine][epsilon][kappa][angle_index]`.|
|epsilons|list|Set of possible values for $\epsilon$, the maximum approximation error between the polynomial $P(x)$ and the function $f(x)$ over the chosen interval. Possible values: {0.1, 0.01, 0.001}.|
|kappas|list|Set of possible values for $\kappa$, which determines the interval for function approximation. Possible values: {1, 5, 50, 100, 250, 500, 1000, 1500}.|
|routines|dict|Specifies the available target subroutines (“qsp” or “qsvt”) for the phase angles.|
|poly|dict|Coefficients of the Chebyshev polynomial $P(x)$ that approximates the function $f(x)$. This is provided as a dictionary of lists, with form `poly[epsilon][kappa][polynomial_index]`.|