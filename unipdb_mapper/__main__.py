 #!/usr/bin/env python3
"""
Entry point for the unipdb_mapper command-line-interface.
This script parses input arguments, invokes the core functionality of the package,
and outputs the results in a CSV file by default.

Usage:
    unipdb [options]

or if not installed:
    python -m unipdb_mapper {idmapper,resmapper} [options]

For help:
    unipdb {idmapper,resmapper} --help
"""

import sys
import argparse
from multiprocessing import Pool
import warnings
from unipdb_mapper import utilities


def main():
    """
    Main function that serves as the entry point for the script.
    """

    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("-p", "--pdb", type=str, nargs="+", default=[], \
        help="PDB ID to map the identifiers or residue position(s) from")
    common_parser.add_argument("-u", "--unp", nargs="+", type=str, default=[], \
        help="UniProt ID to map the identifiers or residue position(s) from")

    parse = argparse.ArgumentParser(description="Tool for ID mapping and residue mapping" \
                        "between UniProt and PDB entries")
    subparsers = parse.add_subparsers(dest="command", required=True)

    idmap_parser = subparsers.add_parser("idmapper", parents=[common_parser], \
                                         help="ID Mapper between UniProt and PDB")
    idmap_parser.add_argument("-o", "--output", type=str, default="output_unipdb-idmapper.csv")

    resmap_parser = subparsers.add_parser("resmapper", parents=[common_parser], \
                                          help="Residue Mapper between UniProt and PDB")
    resmap_parser.add_argument("-n", "--num", type=str, nargs="+", required=True, \
        help="Residue position(s) to map from PDB/UniProt to UniProt/PDB")
    resmap_parser.add_argument("-d", "--dir", type=str, default="SIFTS_XML", \
                               help="Directory to store the SIFTS files")
    resmap_parser.add_argument("-o", "--output", type=str, default="output_unipdb-resmapper.csv")

    args = parse.parse_args()


    if args.pdb and args.unp:
        print("Please provide either the PDB ID or the UniProt ID, and not both of them.")
        sys.exit()
    src_db = 'UniProt' if args.unp else 'PDB'
    entry_ids = args.unp if args.unp else args.pdb

    if args.command == "idmapper" or src_db == "UniProt":
        idmap_args = [(entry, src_db) for entry in entry_ids]
        with Pool() as pool:
            results = pool.starmap(utilities.idmap_worker, (idmap_args))

    if args.command == "resmapper":
        if args.unp and src_db == 'UniProt':
            flat_list = [item for sublist in results for item in sublist]
            query_pdbs = list((x[0], x[3]) for x in flat_list)
        if args.pdb:
            query_pdbs = list((x, x) for x in args.pdb)

        query_pdbs = list(dict.fromkeys(item for item in query_pdbs))

        idmap_args = [(entry[0], entry[1], src_db, args.num) for entry in query_pdbs]
        with Pool() as pool:
            results = pool.starmap(utilities.resmap_worker, (idmap_args))

    flat_list = [item for sublist in results for item in sublist]
    if args.output:
        if len(flat_list) < 1:
            warnings.warn(f"Nothing to write in the file {args.output}")
        else:
            outfile = utilities.output_writer(out_file=args.output, out_data=flat_list)
            print(f"Results have been saved in {outfile}.")

if __name__ == "__main__":
    main()
