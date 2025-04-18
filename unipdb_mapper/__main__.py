 #!/usr/bin/env python3
"""
Entry point for the unipdb_mapper command-line-interface.
This script parses input arguments, invokes the core functionality of the package,
and outputs the results in a CSV file by default.

Usage:
    unipdb [options]

or if not installed:
    python -m unipdb_mapper [options]

For help:
    unipdb --help

"""
import sys
import argparse
from unipdb_mapper import ResiduesMapper

def main():
    """
    Main function that serves as the entry point for the script.
    """
    parse = argparse.ArgumentParser(description=__doc__, \
        formatter_class=argparse.RawDescriptionHelpFormatter,\
        epilog='Tool for residue mapping between UniProt and PDB entries')
    parse.add_argument("-p", "--pdb", type=str, default=[], \
        help="PDB ID to map the residue position(s) from")
    parse.add_argument("-u", "--unp", type=str, default=[], \
        help="UniProt ID to map the residue position(s) from")
    parse.add_argument("-n", "--num", type=int, nargs="+", required=True, \
        help="Residue position(s) to map from PDB/UniProt to UniProt/PDB")
    parse.add_argument("-o", "--out", type=str, default="output.csv", help="Output file name (csv)")
    args = parse.parse_args()

    if args.pdb and args.unp:
        print("Please provide either the PDB ID or the UniProt ID, and not both of them.")
        sys.exit()
    elif args.unp:
        mapper = ResiduesMapper(args.unp.upper(), args.num, src_db='UniProt')
        mapped_residues = mapper.resmapper_unp2pdb()
    elif args.pdb:
        mapper = ResiduesMapper(args.pdb, args.num, src_db='PDB')
        mapped_residues = mapper.resmapper_pdb2unp()
    else:
        print("Please provide either the PDB ID or the UniProt ID. You haven't provided any.")
        sys.exit()

    output = mapper.output_writer(args.out, mapped_residues)
    print(f"The mapping has been written to to the {output} file.")

if __name__ == "__main__":
    main()
