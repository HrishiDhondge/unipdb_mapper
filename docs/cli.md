# Command-line-Interface (CLI) Examples

Once installed, you're all set to start mapping and exploring entry-level and residue-level correspondences between UniProt and PDB entries; no additional setup required!


## Using from Command-Line-Interface

1. Getting help

```bash
$ unipdb -h
usage: unipdb [-h] {idmapper,resmapper} ...

Tool for ID mapping and residue mappingbetween UniProt and PDB
entries

positional arguments:
  {idmapper,resmapper}
    idmapper            ID Mapper between UniProt and PDB
    resmapper           Residue Mapper between UniProt and PDB

options:
  -h, --help            show this help message and exit
```

### ID Mapping

1. Getting help
```bash
$ unipdb idmapper -h
usage: unipdb idmapper [-h] [-p PDB [PDB ...]] [-u UNP [UNP ...]]
                       [-o OUTPUT]

options:
  -h, --help            show this help message and exit
  -p PDB [PDB ...], --pdb PDB [PDB ...]
                        PDB ID to map the residue position(s)
                        from
  -u UNP [UNP ...], --unp UNP [UNP ...]
                        UniProt ID to map the residue position(s)
                        from
  -o OUTPUT, --output OUTPUT
```

2. ID Mapping from UniProt to PDB
```bash
$ unipdb idmapper -u P19339 -o output.csv
Results have been saved in output.csv.
```
Let's see the results with the `cat` command:
```bash
$ cat output.csv
UniProt_ID,UniProt_start_position,UniProt_end_position,PDB_ID,PDB_chain,PDB_start_position,PDB_end_position
P19339,198,294,1sxl,A,1,97
P19339,122,209,2sxl,A,1,88
P19339,122,289,1b7f,A,1,168
P19339,122,289,1b7f,B,1,168
P19339,113,294,3sxl,A,3,184
P19339,113,294,3sxl,B,3,184
P19339,113,294,3sxl,C,3,184
P19339,122,294,4qqb,A,4,176
P19339,122,294,4qqb,B,4,176
```

3. ID Mapping from PDB to UniProt
```bash
$ unipdb idmapper -p 1b7f
Results have been saved in output_unipdb-idmapper.csv.
```
The `output_unipdb-idmapper.csv.` file contain the mapping information:
```bash
cat output_unipdb-idmapper.csv. 
UniProt_ID,UniProt_start_position,UniProt_end_position,PDB_ID,PDB_chain,PDB_start_position,PDB_end_position
P19339,122,289,1b7f,A,1,168
P19339,122,289,1b7f,B,1,168
```

### Resiude Mapping
1. Getting help
```bash
$ unipdb resmapper -h
usage: unipdb resmapper [-h] [-p PDB [PDB ...]]
                        [-u UNP [UNP ...]] -n NUM [NUM ...]
                        [-d DIR] [-o OUTPUT]

options:
  -h, --help            show this help message and exit
  -p PDB [PDB ...], --pdb PDB [PDB ...]
                        PDB ID to map the residue position(s)
                        from
  -u UNP [UNP ...], --unp UNP [UNP ...]
                        UniProt ID to map the residue position(s)
                        from
  -n NUM [NUM ...], --num NUM [NUM ...]
                        Residue position(s) to map from
                        PDB/UniProt to UniProt/PDB
  -d DIR, --dir DIR     Directory to store the SIFTS files
  -o OUTPUT, --output OUTPUT
```

2. Residue Mapping from UniProt to PDB
```bash
$ unipdb resmapper -u P19339 -n 222 123 -o output-resmapper.csv
Results have been saved in output-resmapper.csv.
```
Let's see the results:
```bash
$ cat output-resmapper.csv 
Database,UniProt_ID,UniProt_position,UniProt_residue,Database,PDB_ID,PDB_chain,PDB_position,PDB_residue
UniProt,P19339,222,I,PDB,1sxl,A,25,ILE
UniProt,P19339,123,S,PDB,2sxl,A,2,SER
UniProt,P19339,123,S,PDB,1b7f,A,123,SER
UniProt,P19339,222,I,PDB,1b7f,A,222,ILE
UniProt,P19339,123,S,PDB,1b7f,B,123,SER
UniProt,P19339,222,I,PDB,1b7f,B,222,ILE
UniProt,P19339,123,S,PDB,3sxl,A,null,SER
UniProt,P19339,222,I,PDB,3sxl,A,222,ILE
UniProt,P19339,123,S,PDB,3sxl,B,null,SER
UniProt,P19339,222,I,PDB,3sxl,B,222,ILE
UniProt,P19339,123,S,PDB,3sxl,C,null,SER
UniProt,P19339,222,I,PDB,3sxl,C,222,ILE
UniProt,P19339,123,S,PDB,4qqb,A,123,SER
UniProt,P19339,222,I,PDB,4qqb,A,222,ILE
UniProt,P19339,123,S,PDB,4qqb,B,123,SER
UniProt,P19339,222,I,PDB,4qqb,B,222,ILE
```

3. Residue Mapping from PDB to UniProt
```sh
$ unipdb resmapper -p 1b7f -n 222 123
Results have been saved in output_unipdb-resmapper.csv.
```
The results have been saved in the `output_unipdb-resmapper.csv` file:
```sh
$ cat output_unipdb-resmapper.csv
Database,UniProt_ID,UniProt_position,UniProt_residue,Database,PDB_ID,PDB_chain,PDB_position,PDB_residue
UniProt,P19339,123,S,PDB,1b7f,A,123,SER
UniProt,P19339,222,I,PDB,1b7f,A,222,ILE
UniProt,P19339,123,S,PDB,1b7f,B,123,SER
UniProt,P19339,222,I,PDB,1b7f,B,222,ILE
```

