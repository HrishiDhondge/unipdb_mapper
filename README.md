# UniPDB Residue Mapper 
![Build](https://img.shields.io/github/actions/workflow/status/HrishiDhondge/unipdb_mapper/build_publish.yml?branch=main)
[![PyPI](https://img.shields.io/pypi/v/unipdb_mapper?logo=pypi)](https://pypi.org/project/unipdb-mapper)
![pylint](https://img.shields.io/badge/PyLint-9.57-yellow?logo=python&logoColor=white)
[![Docs](https://readthedocs.org/projects/unipdb-mapper/badge/?version=latest)](https://unipdb-mapper.readthedocs.io/)


<p align="center"><img src="https://github.com/HrishiDhondge/unipdb_mapper/raw/main/docs/logo.png" height="250"/></p>

UniPDB Mapper is a Python package designed for identifier (ID) and residue mapping between UniProt and PDB databases.


## Getting Started
- 🚀 [Installation](https://unipdb-mapper.readthedocs.io/en/latest/installation.html)
- 💲 [Command line examples](https://unipdb-mapper.readthedocs.io/en/latest/cli.html)
- 🐍 [Usage in Python script](https://unipdb-mapper.readthedocs.io/en/latest/scripting.html)
- 📖 [Read the documentation](https://unipdb-mapper.readthedocs.io/)

---


## Installation

```sh
$ pip install unipdb_mapper
```

## Usage
This package can be used either in any of the Python scripts or via the terminal. 

### Usage via Terminal
1. Getting help

```sh
$ unipdb -h
```

2. ID Mapping from UniProt to PDB
```sh
$ unipdb idmapper -u P19339
```

3. ID Mapping from PDB to UniProt
```sh
$ unipdb idmapper -p 1B7F
```

4. Residue Mapping from UniProt to PDB
```sh
$ unipdb resmapper -u P19339 -n 222
```

3. Residue Mapping from PDB to UniProt
```sh
$ unipdb resmapper -p 1B7F -n 222
```


## Questions and Bugs
If you encounter any bugs or have questions about using the software, please don’t hesitate to open an issue on [GitHub](https://github.com/HrishiDhondge/unipdb_mapper.git). Bug reports and suggestions are an important part of making UniPDB Mapper more stable and user-friendly. Your feedback plays a vital role in improving the project.

## News
If you like/use this repository, don't forget to give a star 🌟.

Some exciting updates including detailed examples are planned so stay tuned!!

---
## Acknowledgements
This Project uses APIs provided by [PDBe](https://www.ebi.ac.uk/pdbe/) and extracts information integrated by [SIFTS](https://www.ebi.ac.uk/pdbe/docs/sifts/). 

