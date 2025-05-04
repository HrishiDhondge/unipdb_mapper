# Installation Details

The [UniPDB Mapper][pypi] package is available on the Python Package Index (PyPI). The source code can be found on [GitHub][github].

## Installation 
UniPDB Mapper can be easily installed with just a single command:

```
pip install unipdb_mapper
```

Once installed, you're all set to start mapping and exploring entry-level and residue-level correspondences between UniProt and PDB entries; no additional setup required!

## Building from Source
Install [uv](https://docs.astral.sh/uv/getting-started/installation/), a Python package and project manager:
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Clone the "UniPDB Mapper" repository:
```
https://github.com/HrishiDhondge/unipdb_mapper.git
```

Switch to the unipdb_mapper directory and build the package with uv:
```
uv build
```
This builds the project in the current directory, and place the built artifacts in a `dist/` subdirectory. 

Finally, you may install the `unipdb_mapper` package with `pip` command:
```
pip install dist/unipdb_mapper-<version>-py3-none-any.whl
```
Make sure to replace the `version` with the latest version of the package. 




[pypi]: https://pypi.org/project/unipdb-mapper "PyPI distribution of the UniPDB Mapper"
[github]: https://github.com/HrishiDhondge/unipdb_mapper.git "GitHub source code repository for the UniPDB Mapper project"