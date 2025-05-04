# Using in Python Scripts

Once installed, you're all set to start mapping and exploring entry-level and residue-level correspondences between UniProt and PDB entries; no additional setup required!

## Using in Python Scripts

1. Importing within a Python script
```python
from unipdb_mapper import IDMapper
```

2. ID mapping from UniProt to PDB
```python
id_cls = IDMapper('P19339', 'UniProt')
print(id_cls.mapped)
```

3. ID mapping from PDB to UniProt
```python
id_cls = IDMapper('1b7f', 'PDB')
print(id_cls.mapped)
```

4. Save results to a file
```python
from unipdb_mapper import utilities as utils
outfile = utils.output_writer('output_unipdb.csv', id_cls.mapped)
```


The ID mapping process results in a list of tuples where each tuple is formatted as follows:
```
[(UniProt_ID, UniProt_start_position, UniProt_end_position, PDB_ID, PDB_chain, PDB_start_position, PDB_end_position)]
```
where, the *start_position and *last_position are the first and last residue position available in the mapped structure, respectively. 

## Residue Mapping
1. Importing the classes within a Python script
```python
from unipdb_mapper import IDMapper
from unipdb_mapper import ResidueMapper
```

2. Residue Mapping from UniProt to PDB
```python
id_cls = IDMapper('P19339', 'UniProt')
query_pdbs = [x[3] for x in id_cls.mapped]
mapped_residues = []
for query in query_pdbs:
    res_cls = ResiduesMapper('P19339', ['222'], 'UniProt')
    mapped_residues.append(res_cls.resmapper(query))
results = [item for sublist in mapped_residues for item in sublist]
print(results)
```

3. Residue Mapping from PDB to UniProt
```python
res_cls = ResiduesMapper('1B7F', ['222'], 'PDB')
results = res_cls.resmapper('1B7F')
print(results)
```

4. Save results to a file
```python
from unipdb_mapper import utilities as utils
outfile = utils.output_writer('output_unipdb.csv', results)
```

