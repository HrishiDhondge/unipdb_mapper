 #!/usr/bin/env python3
"""
The class for residue mapping from PDB to UniProt and Vice-versa.
"""

from urllib.request import urlopen
import os
import json
import argparse
import sys
import wget
from bs4 import BeautifulSoup
from sh import gunzip

class ResiduesMapper():
    """
    Class for mapping the residue numbering between PDB <--> UniProt residues
    """

    def __init__(self, src_id, res_pos, db=str, path=None):
        self.src_id = src_id
        self.db = db
        self.res_pos = [res_pos] if isinstance(res_pos, int) else res_pos
        assert isinstance(self.res_pos[0], int), "The residue positions passed are not integers"
        self.path = os.path.join(os.getcwd(), 'tmpdir') if path is None else path
        os.makedirs(self.path, exist_ok=True)

        if self.db == 'UniProt':  # to get numbering for PDB residues from UniProt
            self.mapped = self.unp2pdb_api()
        elif self.db == 'PDB':  # to get numbering for UniProt residues from PDB
            self.mapped = self.pdb2unp_api()
        else:
            print("Please provide the correct database name: {'UniProt', 'PDB'}.")
            sys.exit()

    def unp2pdb_api(self):
        """
        Function to map uniprot ids to corresponding pdb ids with chains
        :return: list of tuples :[('1B7F', 'A', 'P19339'), ('1B7F', 'B', 'P19339')]
        """
        url = "https://www.ebi.ac.uk/pdbe/api/mappings/all_isoforms/" + self.src_id
        with urlopen(url) as response:
            data_dict = json.loads(response.read())[self.src_id.upper()]['PDB']
        new_dict = []
        for pdb in list(data_dict.keys()):
            if '-' in pdb:
                continue
            new_dict.extend([(self.src_id.upper(), pdb, x['chain_id']) for x in data_dict[pdb]])
        assert len(new_dict) > 0, "The given UniProt ID can not be mapped to any PDB Ids"
        return new_dict

    def pdb2unp_api(self):
        """
        Function to get all chain ids and map the pdb ids to corresponding uniprot ids
        :return: list of tuples :[('1B7F', 'A', 'P19339'), ('1B7F', 'B', 'P19339')]
        """
        url = "https://www.ebi.ac.uk/pdbe/api/mappings/all_isoforms/" + self.src_id
        with urlopen(url) as response:
            data_dict = json.loads(response.read())[self.src_id.lower()]['UniProt']

        new_dict = []
        for unp in list(data_dict.keys()):
            if '-' in unp:
                continue
            new_dict.extend([(self.src_id, x['chain_id'], unp) for x in data_dict[unp]['mappings']])
        assert len(new_dict) > 0, "The given PDB ID can not be mapped to any UniProt Ids"
        return new_dict

    def get_sifts_file(self, pdb_code):
        """
        Download residue mapping files from SIFTS (.xml)
        :param pdb_code: Protein Data Bank (PDB) identifier
        :return: Nothing
        """
        # prev_url = 'ftp://ftp.ebi.ac.uk/pub/databases/msd/sifts/xml/'+pdb_code.upper()+'.xml.gz'
        url = 'https://ftp.ebi.ac.uk/pub/databases/msd/sifts/xml/' + pdb_code.lower() + '.xml.gz'
        wget.download(url, out=self.path)
        gunzip(os.path.join(self.path, pdb_code.lower() + '.xml.gz'))

    def gather_residues_xml(self, pdb=None):
        """
        Download SIFTS file if not already & collect all the residue entities together
        :param pdb: Protein Data Bank (PDB) identifier
        :return: all residue elements gathered from SIFTS file
        """
        pdb = pdb if pdb is not None else self.src_id
        if pdb + '.xml' not in os.listdir(self.path):
            self.get_sifts_file(pdb)

        # Reading the xml file
        with open(os.path.join(self.path, pdb + '.xml'), 'r', encoding='utf-8') as file_xml:
            data = file_xml.read()
        data = BeautifulSoup(data, "xml")
        entity = data.find_all('entity')

        all_res = []
        for one in entity:  # get all residues at one place to iterate over
            part = one.find_all('residue')
            if len(all_res) == 0:
                all_res = part
                continue
            all_res.extend(part)
        return all_res

    def resmapper_unp2pdb(self, pdb=None, chain=None):
        """
        Residue mapping is done using this function (UniProt --> PDB)
        :param pdb: Protein Data Bank (PDB) identifier
        :param chain: chain identifier from the given PDB structure
        :return: list of tuples
        """
        if pdb is not None:
            self.mapped = [x for x in self.mapped if x[1].lower() == pdb.lower()]
        if chain is not None:
            self.mapped = [x for x in self.mapped if x[2] == chain]
        uni_res_pos_list = [str(a) for a in self.res_pos]
        query_pdbs = list({x[1].upper() for x in self.mapped})

        final = []
        for pdb_id in query_pdbs:
            residues = self.gather_residues_xml(pdb=pdb_id.lower())

            # looking for list of residue numbers (int) from example
            for residue in residues:
                crossref = residue.find_all('crossRefDb')
                pdb = [aa for aa in crossref if aa.get('dbSource') == 'PDB']
                pdb = None if len(pdb) < 1 else pdb[0]
                uniprot = [aa for aa in crossref if aa.get('dbSource') == 'UniProt']
                uniprot = None if len(uniprot) < 1 else uniprot[0]

                if (uniprot is not None) and (uniprot.get('dbAccessionId') == self.src_id) and \
                        (uniprot.get('dbResNum') in uni_res_pos_list):
                    tmp_tup = (uniprot.get('dbSource'), uniprot.get('dbAccessionId'), \
                               uniprot.get('dbResNum'), uniprot.get('dbResName'))
                    tmp_tup += ('PDB', pdb_id, None, None, None) if pdb is None else \
                        (pdb.get('dbSource'), pdb.get('dbAccessionId'), pdb.get('dbChainId'), \
                         pdb.get('dbResNum'), pdb.get('dbResName'))

                    final.append(tmp_tup)

        assert len(final) > 0, (
            f"The given residue position(s) is not present in any of the "
            f"PDB structures {', '.join(query_pdbs)}"
            )
        return final

    def resmapper_pdb2unp(self, chain=None):
        """
        Residue mapping is done using this function (PDB --> UniProt)
        :param chain: chain identifier from the given PDB structure
        :return: list of tuples[('UniProt', 'P19339', '253', 'G', 'PDB', '1b7f', 'A', '253', 'GLY')]
        """
        self.src_id = self.src_id.lower()
        if chain is not None:
            self.mapped = [x for x in self.mapped if x[1] == chain]
        pdb_res_pos_list = [str(x) for x in self.res_pos]

        residues = self.gather_residues_xml()
        final = []
        # looking for list of residue numbers (int) from example
        for residue in residues:
            crossref = residue.find_all('crossRefDb')

            pdb = [aa for aa in crossref if aa.get('dbSource') == 'PDB']
            pdb = None if len(pdb) < 1 else pdb[0]
            uniprot = [aa for aa in crossref if aa.get('dbSource') == 'UniProt']
            uniprot = None if len(uniprot) < 1 else uniprot[0]
            if (pdb is not None) and (pdb.get('dbResNum') != 'null') and (pdb.get('dbResNum') \
                                                                          in pdb_res_pos_list):
                tmp_tup = ('UniProt', None, None, None) if uniprot is None else \
                    (uniprot.get('dbSource'), uniprot.get('dbAccessionId'), \
                     uniprot.get('dbResNum'), uniprot.get('dbResName'))

                tmp_tup += (pdb.get('dbSource'), pdb.get('dbAccessionId'), pdb.get('dbChainId'), \
                            pdb.get('dbResNum'), pdb.get('dbResName'))
                final.append(tmp_tup)

        assert len(final) > 0, (
            f"The given residue position(s) is not present in any chain:"
            f"{', '.join(list({x[1].upper() for x in self.mapped}))}"
            )
        return final
    
    def output_writer(self, out_file=str, out_data=list):
        """
        Writes the mapped residues to the output file in CSV format
        """
        out_header = ["Database", "UniProt_ID", "UniProt_position", "UniProt_residue", "Database", \
                "PDB_ID", "PDB_chain", "PDB_position", "PDB_resiude"]

        with open(out_file, 'w', encoding="utf8") as wrt:
            wrt.write(",".join(out_header))
            for tup in out_data:
                wrt.write("\n" + ",".join(tup))
            wrt.close()
        return out_file


    def __str__(self):
        return f'{self.src_id} can be mapped to as follows: {self.mapped}'

if __name__ == "__main__":
    P = argparse.ArgumentParser(description=__doc__, \
        formatter_class=argparse.RawDescriptionHelpFormatter,\
        epilog='Writes the user-given family Ids to a file')
    P.add_argument("-p", "--pdb", type=str, default=[], \
        help="PDB ID to map the residue position(s) from")
    P.add_argument("-u", "--unp", type=str, default=[], \
        help="UniProt ID to map the residue position(s) from")
    P.add_argument("-n", "--num", type=int, nargs="+", required=True, \
        help="Residue position(s) to map from PDB/UniProt to UniProt/PDB")
    P.add_argument("-o", "--out", type=str, default="output.csv", help="Output file name (json)")
    ARGS = P.parse_args()

    if ARGS.pdb and ARGS.unp:
        print("Please provide either the PDB ID or the UniProt ID, and not both of them.")
        sys.exit()
    elif ARGS.unp:
        M = ResiduesMapper(ARGS.unp.upper(), ARGS.num, db='UniProt')
        MAP = M.resmapper_unp2pdb()
    elif ARGS.pdb:
        M = ResiduesMapping(ARGS.pdb, ARGS.num, db='PDB')
        MAP = M.resmapper_pdb2unp()
    else:
        print("Please provide either the PDB ID or the UniProt ID. You haven't provided any.")
        sys.exit()

    output = M.output_writer(ARGS.out, MAP)
    print(f"The mapping has been written to to the {ARGS.out} file.")
