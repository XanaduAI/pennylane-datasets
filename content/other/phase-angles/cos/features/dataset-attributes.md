|Name|Type|Description|
|-|-|-|
|angles|dict|Angles that apply the polynomial transformation for a given routine. This is provided as a dictionary of lists with form `angles[routine][epsilon][k]`.|
|epsilons|list|Set of possible values for $\epsilon$, the maximum approximation error between the polynomial $P(x)$ and the function $f(x)$ over the chosen interval. Possible values: {0.1, 0.01, 0.001}.|
|k|list|Set of possible values for $k$, which determines the period of the function. Possible values: {0, 1, 2, 3, 4, 5, 6, 7}.|
|routines|dict|Specifies the available target subroutines (“qsp” or “qsvt”) for the phase angles.|
|poly|dict|Coefficients of the Chebyshev polynomial $P(x)$ that approximates the function $f(x)$. This is provided as a dictionary of lists, with form `poly[epsilon][k]`.|