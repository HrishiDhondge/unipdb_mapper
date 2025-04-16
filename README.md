# UniPDB Residue Mapper 
![PyPI](https://img.shields.io/pypi/v/unipdb_mapper?label=pypi%20package)
![PyPI - Downloads](https://img.shields.io/pypi/dm/unipdb_mapper)
![pylint]()

<p align="center"><img src="https://github.com/HrishiDhondge/unipdb_mapper/raw/main/.github/unipdb_mapper.png" height="250"/></p>

This package maps residue numbering from UniProt/PDB to PDB/UniProt. 

## Install

```
pip install unipdb_mapper
```

## Usage
This package can be used either in any of the Python scripts or via the terminal. 

### Usage via Python Script

1. Importing within a Python script
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

### Usage via Terminal
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
$ unipdb -p 1b7f -n 122 123 156 -o abc.csv
```


## News
If you like/use this repository, don't forget to give a star 🌟.

Some exciting updates including examples are planned so stay tuned!!
