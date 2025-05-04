# UniPDB Residue Mapper 
![Build](https://img.shields.io/github/actions/workflow/status/HrishiDhondge/unipdb_mapper/pylint.yml?branch=main)
[![PyPI](https://img.shields.io/pypi/v/unipdb_mapper?logo=pypi)](https://pypi.org/project/unipdb-mapper)
![pylint](https://img.shields.io/badge/PyLint-9.71-yellow?logo=python&logoColor=white)

<p align="center"><img src="https://github.com/HrishiDhondge/unipdb_mapper/raw/main/docs/logo.png" height="250"/></p>

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
$ unipdb -p 1b7f -n 122 123 156 -o another_output.csv
```


## News
If you like/use this repository, don't forget to give a star 🌟.

Some exciting updates including examples are planned so stay tuned!!
