This dataset contains a portion of [HamLib](https://quantum-journal.org/papers/q-2024-12-11-1559/): a library of Hamiltonians for benchmarking quantum algorithms and hardware.
The original data can be downloaded from the [authors' source](https://portal.nersc.gov/cfs/m888/dcamps/hamlib/binaryoptimization/max3sat/random/).

**Description of the dataset**

[Max-3-SAT](https://en.wikipedia.org/wiki/MAX-3SAT) is the maximum satisfiability problem with at most 3 variables per clause.
This problem asks "What is the maximum number of clauses that we can satisfy?"

To understand what this means, let's define the system we are working with. Imagine we have a set of boolean variables. 
This can be any number of variables ($x_0, x_1, ..., x_n$) that take a ``True``/``False`` value.
We are told that we have to assign values of ``True`` or ``False`` to each
variable such that we satisfy some criteria, where the criteria are
defined in *clauses*. In Max-3-SAT, the clauses are of the form
$(x_0 \lor x_1 \lor \neg x_2)$, where three variables
appear in each clause. Note that $\lor$ is the symbol for a logical OR operator and
$\neg$ is the symbol for a logical NOT operator.

The Max-3-SAT problem is finding an assignment of variables
that maximize the number of clauses that evaluate to ``True``.

The values of the variables are encoded into qubits by providing one qubit for each variable.
Variable $x_i$ corresponds to qubit $q_i$. We use a qubit state of $|0\rangle$ as ``False`` and $|1\rangle$ as ``True``.
For example: a qubit register in the state $|0010\rangle$ means we have four variables. $x_0$ is ``False`` and $x_2$ is ``True``.
The cost function for a Max-3-SAT problem can then be encoded into a Hamiltonian $H$.
If we encode the problem correctly, then the number of clauses satisfied by a bitstring $|0010\rangle$ is $\langle 0010|H|0010\rangle$.

This dataset contains Hamiltonians for several Max-3-SAT problems.
Each Hamiltonian acts as the cost function for its corresponding Max-3-SAT problem.

**Additional details**

- The problems range from 4 to 900 variables.
  This corresponds to 4 to 900 qubits when encoded in a Hamiltonian.
  Note that any circuit with 20 or more qubits can be computationally expensive to simulate. 
- The number of clauses ranges from 8 to 4500.

**Example usage**

```python
[ds] = qml.data.load("hamlib-max3sat")
ham = ds.hamiltonians[1320]

dev = qml.device("default.qubit", wires=4)

@qml.qnode(dev)
def circuit(basis_state):
    qml.BasisStatePreparation(basis_state, wires=range(4))
    return qml.expval(ham)

# clauses satisfied when all variables are false
circuit([0,0,0,0]) # output: array(7.)
# clauses satisfied when some variables are true
circuit([0,0,1,1]) # output: array(5.)
```
