This dataset contains the data used to train the RydbergGPT LLM model,
developed and trained by the Perimeter Institute Quantum Intelligence Lab and
collaborators. The full dataset on-disk, uncompressed, is about 25 GB.
The model is a vanilla encoder-decoder transformer architecture, which
generates projective measurement samples of a Rydberg atom array system,
conditioned on the Hamiltonian parameters.

**Description of the dataset**

We produce QMC samples of the projective measurement outcomes at points in
the parameter space, defined by the Hamiltonian parameter set
x = {Ω, δ/Ω, R /Ω, β/Ω} . These points are all combinations of the following
b
values:
R b ∈ [1.05, 1.15, 1.30]
δ ∈ [−0.36, −0.13, 0.93, 1.05, 1.17, 1.29, 1.52, 1.76, 2.94, 3.17]
β ∈ [0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 48.0, 64.0]
QMC samples are generated for linear system sizes L ∈ [5, 6, 11, 12, 15, 16] .
We fix Ω = 1.0 for all datasets.
So, there are 1890 parameter points in total.

**Additional details**

- The size of dataset.npy changes for different values of L ; ranging from
2.5 MB for L = 5 (the smallest system size) to 25 MB for L = 16 (thelargest system size).
- config.json is the same size for all parameter directories, at 100 bytes.
- graph.json ranges from 18 kB to 2.1 MB across system sizes.
- For all datapoints in L ∈ [5, 6, 11, 12, 15, 16] , the current total disk space
required (uncompressed) is 23.1 GB.
- The most natural way to partition the data is by system size, L . Total disk
space for L = 5 (smallest system) is 679 MB, total disk space for L = 16 is
7.5 GB.
- Within that, we can also break down by the other three parameters, for
more fine-tuned control over which parameter datasets are
requested/downloaded.

**Example usage**

```python
[ds] = qml.data.load("other", name="rydberggpt")

@qml.qnode(qml.device('default.qubit'))
def circuit(training_circuit):

    for op in ds.circuits[0]:
        qml.apply(op)

    return qml.expval(qml.PauliZ(wires=3)) #measurement on wire 3

circuit(0) # output: tensor(0.04148455, requires_grad=True)
```
