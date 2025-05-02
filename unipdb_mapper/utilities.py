#!/usr/bin/env python3
"""
Utility functions for the UniPDB-mapper
"""
from unipdb_mapper import residue_mapper
from unipdb_mapper import id_mapper

def idmap_worker(entry_ids, entry_db):
    """
    Wrapper function around id_mapper.IDMapper class to use multiprocessing
    """
    id_cls = id_mapper.IDMapper(entry_ids, entry_db)
    return id_cls.mapped

def resmap_worker(entry, pdb_entry, database, positions):
    """
    Wrapper function around residue_mapper.resmapper method to use multiprocessing
    """
    entry = pdb_entry if database == 'PDB' else entry
    resmap = residue_mapper.ResiduesMapper(src_id=entry, src_db=database, res_pos=positions)
    mapped_residues = resmap.resmapper(pdb_id=pdb_entry)
    return mapped_residues

def output_writer(out_file=str, out_data=list):
    """
    Writes the mapped residues to the output file in CSV format
    """
    id_header = ["UniProt_ID", "UniProt_start_position", "UniProt_end_position", "PDB_ID", \
                  "PDB_chain", "PDB_start_position", "PDB_end_position"]
    res_header = ["Database", "UniProt_ID", "UniProt_position", "UniProt_residue", "Database", \
                  "PDB_ID", "PDB_chain", "PDB_position", "PDB_residue"]
    out_header = id_header if len(out_data[0]) == 7 else res_header

    with open(out_file, 'w', encoding="utf8") as wrt:
        wrt.write(",".join(out_header))
        for tup in out_data:
            wrt.write("\n" + ",".join(map(str, tup)))
        wrt.close()
    return out_file
