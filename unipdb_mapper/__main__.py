 #!/usr/bin/env python3
import sys
import argparse
from unipdb_mapper import ResiduesMapper

def main():
    P = argparse.ArgumentParser(description=__doc__, \
        formatter_class=argparse.RawDescriptionHelpFormatter,\
        epilog='Tool for residue mapping between UniProt and PDB entries')
    P.add_argument("-p", "--pdb", type=str, default=[], \
        help="PDB ID to map the residue position(s) from")
    P.add_argument("-u", "--unp", type=str, default=[], \
        help="UniProt ID to map the residue position(s) from")
    P.add_argument("-n", "--num", type=int, nargs="+", required=True, \
        help="Residue position(s) to map from PDB/UniProt to UniProt/PDB")
    P.add_argument("-o", "--out", type=str, default="output.csv", help="Output file name (csv)")
    ARGS = P.parse_args()

    if ARGS.pdb and ARGS.unp:
        print("Please provide either the PDB ID or the UniProt ID, and not both of them.")
        sys.exit()
    elif ARGS.unp:
        M = ResiduesMapper(ARGS.unp.upper(), ARGS.num, db='UniProt')
        MAP = M.resmapper_unp2pdb()
    elif ARGS.pdb:
        M = ResiduesMapper(ARGS.pdb, ARGS.num, db='PDB')
        MAP = M.resmapper_pdb2unp()
    else:
        print("Please provide either the PDB ID or the UniProt ID. You haven't provided any.")
        sys.exit()

    output = M.output_writer(ARGS.out, MAP)
    print(f"The mapping has been written to to the {output} file.")

if __name__ == "__main__":
    main()
