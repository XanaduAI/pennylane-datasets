Data for benchmarking machine learning models, taken from
[Train on classical, deploy on quantum: scaling generative quantum machine learning to a thousand qubits](https://arxiv.org/abs/2503.02934).
This dataset contains data that corresponds to alleles at 805 highly differentiated biallelic single
nucleotide polymorphisms (SNPs) of the human genome. The dataset was taken from the paper
[Creating artificial human genomes using generative neural networks](https://pmc.ncbi.nlm.nih.gov/articles/PMC7861435/). 


**Description of the dataset**

The dataset contains bit strings of length 805, with the presence of a 1 at a given
location marking the presence of the variant allele in that individual. The dataset was constructed from
genetic data from 2504 individuals from the 1000 genomes project, which results in a
dataset of size 5008 (since each individual has two haplotypes). There are 3338 training inputs 
and 1670 testing inputs. 

**Example usage**

```python
[ds] = qml.data.load("other", name="genomic)

ds.train
ds.test
```
