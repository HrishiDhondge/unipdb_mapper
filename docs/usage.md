# Usage Examples

The [UniPDB Mapper][pypi] package is available on the Python Package Index (PyPI). The source code can be found on [GitHub][github].

## Installation
UniPDB Mapper can be easily installed with just a single command:

```
pip install unipdb_mapper
```

Once installed, you're all set to start mapping and exploring entry-level and residue-level correspondences between UniProt and PDB entries; no additional setup required!

## Using in Python Scripts

1. Importing the Package
```
from unipdb_mapper import ResiduesMapper
```

2. Residue Mapping from UniProt to PDB
```
M = ResiduesMapper('P19339', [122, 145], 'UniProt')
MAP = M.resmapper_unp2pdb()
print(MAP)
```

3. Residue Mapping from PDB to UniProt

```
M = ResiduesMapper('1b7f', [123, 145], 'PDB')
MAP = M.resmapper_pdb2unp()
print(MAP)
```

4. Save results to a file
```
OUTFILE = M.output_writer('output.csv', MAP)
```

## Using from Command-Line-Interface

1. Getting help

```
$ unipdb -h
```

2. Residue Mapping from UniProt to PDB
```
$ unipdb -u P19339 -n 122 123 156 -o output.csv
```

3. Residue Mapping from PDB to UniProt
```
$ unipdb -p 1b7f -n 122 123 156 -o another_output.csv
```


## Learn more

We are working on adding more detailed examples soon.


[pypi]: https://pypi.org/project/unipdb-mapper "PyPI distribution of the UniPDB Mapper"
[github]: https://github.com/HrishiDhondge/unipdb_mapper.git "GitHub source code repository for the UniPDB Mapper project"