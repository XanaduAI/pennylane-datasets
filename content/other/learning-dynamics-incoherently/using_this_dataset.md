This dataset contains data from [The power and limitations of learning quantum dynamics incoherently](https://arxiv.org/abs/2303.12834)
by Jerbi S., Gibbs J., Rudolph M. S., et al.
It includes initial states, a Hamiltonian to evolve these states, and the
resulting [classical shadow data](https://docs.pennylane.ai/en/stable/code/api/pennylane.classical_shadow.html) measured from the circuits.
These can be used to train a variational quantum circuit that simulates the dynamics of the Hamiltonian, as done in the paper.

**Description of the dataset**

If we had several known input states, applied an unknown quantum operator to them, and sampled measurements from
the final states, could we reproduce the unknown operator? How hard would it be? 

These questions are addressed in detail by Jerbi et al.
They demonstrate one way to reproduce the unknown operator is to train a variational quantum circuit that learns to produce the same output.

This dataset provides data used by the authors to demonstrate this method. 
For this demonstration, two training states were drawn from the [Haar random distribution](https://pennylane.ai/qml/demos/tutorial_haar_measure/)
as initial states. A variational quantum circuit was applied to these initial states and its parameters were optimized with respect to a cost function
(see equation 5).
After optimization, the output of the variational circuit approximated the output of a target Trotterized transverse-field Ising Hamiltonian.

This dataset provides the information required to reproduce the training in the paper. It includes:

- 16-qubit initial states for training. These are provided as state vectors and as circuits that prepare the state vectors.
- The transverse-field Ising Hamiltonian for evolving the training states. This is provided as a [PennyLane Hamiltonian](https://docs.pennylane.ai/en/stable/code/api/pennylane.Hamiltonian.html)
  and as a list of the magnetic field strengths on each spin/qubit.
- The classical shadow measurement samples obtained by sampling the 16-qubit quantum states after evolution with the above Hamiltonian.
  This is provided as two lists, one describing the type of measurement and the other describing
  the measurement result.

**Additional details**

- This dataset contains 280,500 classical shadow measurements for each input state.
- Classical shadow measurements are obtained from a quantum computer by applying a Trotterized
  form of the transverse-field Ising Hamiltonian to the initial states and sampling the output.
- Classical shadow measurements were performed on the superconducting qubit IBM quantum computer ``ibmq_kolkata``.
- Classical shadow measurements and bases use the same conventions as in [PennyLane classical shadows](https://docs.pennylane.ai/en/stable/code/qml_shadows.html). 
  I.e., in bases, ``0`` corresponds to Pauli X, ``1`` corresponds to Pauli Y, and ``2`` corresponds to Pauli Z.
- For details on the cost function used for training, see appendix B in [the paper](https://arxiv.org/abs/2303.12834).

**Example usage**

To create a circuit that reproduces the system measured in the paper:

```python
[ds] = qml.data.load("other", name="learning-dynamics-incoherently")

@qml.qnode(qml.device('default.qubit'))
def circuit(training_circuit):
    # apply circuit to get \psi, the state sampled from a Haar random distribution
    for operation in ds.training_circuits[0]:
        qml.apply(operation)

    # apply first-order, 1-step, Trotterized hamiltonian evolution for time=0.1
    qml.TrotterProduct(ds.hamiltonian, time=0.1, n=1,order=1)

    return qml.expval(qml.PauliZ(wires=0))

circuit(0) # output: tensor(-0.46754745, requires_grad=True)
```

To obtain estimated expectation values using the shadow measurements in this dataset:

```python
bits = ds.shadow_meas[0]
recipes = ds.shadow_bases[0]
cs = qml.ClassicalShadow(bits, recipes)

cs.expval(qml.PauliZ(wires=0)) # output: array(-0.26416043)
```
