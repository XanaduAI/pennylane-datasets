|Name|Type|Description|
|-|-|-|
|angles|dict|Specific angles which apply the polynomial transformation for a specific routine. This is provided as a dictionary of form `angles[routine][epsilon][kappa]`.|
|epsilons|list|Set of possible values for $\epsilon$, the maximum approximation error between the polynomial $P(x)$ and the function $f(x)$ over the chosen interval. Possible values: {0.1, 0.01, 0.001}.|
|kappas|list|Set of possible values for $\kappa$, which determines the interval for function approximation. Possible values: {1, 5, 50, 100, 250, 500, 1000, 1500}.|
|routines|dict|Specifies the target subroutines (“qsp” or “qsvt”) where the phase angles to implement the polynomial transformation P(x) will be used.|
|poly|dict|Coefficients of the polynomial P(x) that approximates the function f(x)|