 #!/usr/bin/env python3
"""
The class for id mapping (entries) between UniProt and PDB.
"""

from urllib.request import urlopen
import json
import sys
import warnings

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
            warnings.warn("Please provide the correct database name: {'UniProt', 'PDB'}.",
                          UserWarning)
            sys.exit()

    def unp2pdb_api(self):
        """
        Function to map uniprot ids to corresponding pdb ids with chains
        :return: list of tuples :[('P19339', '198', '294', '1sxl', 'A', '1', '97')]
        """
        url = "https://www.ebi.ac.uk/pdbe/api/mappings/all_isoforms/" + self.src_id
        try:
            with urlopen(url) as response:
                data_dict = json.loads(response.read())[self.src_id.upper()]['PDB']
        except Exception as err:
            warnings.warn(
                (f"The given UniProt ID '{self.src_id}' can not be mapped to any PDB IDs. {err}"),
                UserWarning)
            return []

        tmp_list = []
        for pdb in list(data_dict.keys()):
            if '-' in pdb:
                continue
            tmp_list.extend([(self.src_id.upper(),  x['unp_start'], x['unp_end'], pdb, \
                            x['chain_id'], x['start']['residue_number'], \
                                x['end']['residue_number']) for x in data_dict[pdb]])
        return tmp_list

    def pdb2unp_api(self):
        """
        Function to get all chain ids and map the pdb ids to corresponding uniprot ids
        :return: list of tuples :[('P19339', '198', '294', '1sxl', 'A', '1', '97')]
        """
        url = "https://www.ebi.ac.uk/pdbe/api/mappings/all_isoforms/" + self.src_id
        try:
            with urlopen(url) as response:
                data_dict = json.loads(response.read())[self.src_id.lower()]['UniProt']
        except Exception as err:
            warnings.warn(
                (f"The given PDB ID '{self.src_id}' can not be mapped to any UniProt IDs. {err}"),
                UserWarning)
            return []

        tmp_list = []
        for unp in list(data_dict.keys()):
            if '-' in unp:
                continue
            tmp_list.extend([(unp, x['unp_start'], x['unp_end'], self.src_id, x['chain_id'], \
                            x['pdb_start'], x['pdb_end']) for x in data_dict[unp]['mappings']])
        return tmp_list


    def __str__(self):
        return f'{self.src_id} can be mapped to as follows: {self.mapped}'
