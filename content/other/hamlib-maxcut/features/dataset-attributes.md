|Name|Type|Description|
|-|-|-|
|`edges`|`list`|The MaxCut edges provided as tuples of form (node1, node2).|
|`hamiltonians`|`list`|List of hamiltonians. Each Hamiltonian corresponds to one MaxCut instance.|
|`ids`|`list`|Describes the graph type. For circulant graphs, these describe the offset in edge connections and have form `circ_offsets-{distance to first connection}-{distance to second connection}`. For complete bipartite graphs, these describe the number of nodes in each set and have form `complbipart_a-{number of nodes in set a}_b{number of nodes in set b}`. Star graphs do not contain extra information and are labeled `star`.|
|`ns`|`list`|List containing the number of nodes for each maxcut instance.|