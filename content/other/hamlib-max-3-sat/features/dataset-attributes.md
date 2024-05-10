|Name|Type|Description|
|-|-|-|
|`clauses`|`pennylane.data.attributes.list.DatasetList`|Lists of clauses for each Max-3-SAT problem. Each clause is a list of three numbers. A value of n means that this refers to the nth variable. A positive value means that the variable must be true to satisfy the clause while a negative value means that variable must be false to satisfy the clause.|
|`hamiltonians`|`pennylane.data.attributes.list.DatasetList`|List of hamiltonians. Each Hamiltonian corresponds to one Max-3-SAT problem.|
|`ids`|`pennylane.data.attributes.list.DatasetList`|List of full names identifying the Max-3-SAT problems.|
|`instanceids`|`pennylane.data.attributes.list.DatasetList`|List containing numbers that identify a specific Max-3-SAT problem within a set of problems that have the same ratio and number of variables.|
|`ns`|`pennylane.data.attributes.list.DatasetList`|List containing the number of variables for each maxsat problem.|
|`ratios`|`pennylane.data.attributes.list.DatasetList`|List of clause ratios r = m/n, where m is the number of clauses and n is the number of variables.|