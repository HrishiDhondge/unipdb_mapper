 #!/usr/bin/env python3
"""
The class for id mapping (entries) between UniProt and PDB.
"""

from urllib.request import urlopen
import json
import sys

class IDMapper():
    """
    Class for mapping the IDs between PDB and UniProt databases.
    """

    def __init__(self, src_id, src_db=str, src_chain=None):
        self.src_id = src_id
        self.src_db = src_db
        self.src_chain = [] if src_chain is None else src_chain

        if self.src_db == 'UniProt':  # to get numbering for PDB residues from UniProt
            self.mapped = self.unp2pdb_api()
        elif self.src_db == 'PDB':  # to get numbering for UniProt residues from PDB
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
        new_list = []

        for pdb in list(data_dict.keys()):
            if '-' in pdb:
                continue
            new_list.extend([(self.src_id.upper(),  x['unp_start'], x['unp_end'], pdb, \
                            x['chain_id'], x['start']['residue_number'], \
                                x['end']['residue_number']) for x in data_dict[pdb]])
        assert len(new_list) > 0, "The given UniProt ID can not be mapped to any PDB Ids"
        return new_list

    def pdb2unp_api(self):
        """
        Function to get all chain ids and map the pdb ids to corresponding uniprot ids
        :return: list of tuples :[('1B7F', 'A', 'P19339'), ('1B7F', 'B', 'P19339')]
        """
        url = "https://www.ebi.ac.uk/pdbe/api/mappings/all_isoforms/" + self.src_id
        with urlopen(url) as response:
            data_dict = json.loads(response.read())[self.src_id.lower()]['UniProt']

        new_list = []

        for unp in list(data_dict.keys()):
            if '-' in unp:
                continue
            new_list.extend([(unp, x['unp_start'], x['unp_end'], self.src_id, x['chain_id'], \
                            x['pdb_start'], x['pdb_end']) for x in data_dict[unp]['mappings']])

        assert len(new_list) > 0, "The given PDB ID can not be mapped to any UniProt Ids"

        return new_list


    def __str__(self):
        return f'{self.src_id} can be mapped to as follows: {self.mapped}'
