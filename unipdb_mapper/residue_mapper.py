 #!/usr/bin/env python3
"""
The class for residue mapping from UniProt to PDB and Vice-versa.
"""

import os
import warnings
import re
import wget
from bs4 import BeautifulSoup
from sh import gunzip

class ResiduesMapper():
    """
    Class for mapping the residue numbering between PDB <--> UniProt residues
    """

    def __init__(self, src_id, res_pos, src_db, path=None):
        self.src_id = src_id
        # self.mapped = mapped
        self.res_pos = res_pos
        self.path = os.path.join(os.getcwd(), 'SIFTS_XML') if path is None else path
        os.makedirs(self.path, exist_ok=True)

        # Checking the source database
        self.src_db = src_db
        assert self.src_db in ['UniProt', 'PDB'], (
            "Please provide the correct database name: {'UniProt', 'PDB'}."
        )

        # Checking the positions to map
        pattern = r'\d+[a-zA-Z]?$'
        invalid_pos = [val for val in self.res_pos if not re.fullmatch(pattern, val)]
        assert not invalid_pos, f"Invalid residue position(s) provided: {invalid_pos}"

        self.inp_dict = {'src': self.src_id, 'query_pos': self.res_pos, 'target': 'UniProt'}
        # print(self.src_id, self.inp_dict)

    def get_sifts_file(self, pdb_code):
        """
        Download residue mapping files from SIFTS (.xml)
        :param pdb_code: Protein Data Bank (PDB) identifier
        :return: Nothing
        """
        url = 'https://ftp.ebi.ac.uk/pub/databases/msd/sifts/xml/' + pdb_code.lower() + '.xml.gz'
        wget.download(url, out=self.path, bar=None)
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


    def resmapper(self, pdb_id=None, res_posi=None):
        """
        Residue mapping is done using this function (UniProt <--> PDB)
        :param pdb: Protein Data Bank (PDB) identifier
        :param chain: chain identifier from the given PDB structure
        :return: list of lists composed of tuples
        """
        query_res_positions = [str(x) for x in self.res_pos] if res_posi is None else res_posi

        final = []
        residues = self.gather_residues_xml(pdb=pdb_id.lower())

        lambda_eval = { 'PDB': lambda: (pdb is not None) and (pdb.get('dbResNum') != 'null') \
                and (pdb.get('dbResNum') in query_res_positions),
            'UniProt': lambda: (uniprot is not None) and (uniprot.get('dbAccessionId') == \
                self.src_id) and (uniprot.get('dbResNum') in query_res_positions)
        }

        # looking for list of residue numbers (str) from xml file
        for residue in residues:
            crossref = residue.find_all('crossRefDb')

            pdb = [aa for aa in crossref if aa.get('dbSource') == 'PDB']
            pdb = None if len(pdb) < 1 else pdb[0]

            uniprot = [aa for aa in crossref if aa.get('dbSource') == 'UniProt']
            uniprot = None if len(uniprot) < 1 else uniprot[0]

            if (self.src_db == 'PDB') and (lambda_eval['PDB']()):
                tmp_tup = ('UniProt', None, None, None) if uniprot is None else \
                    (uniprot.get('dbSource'), uniprot.get('dbAccessionId'), \
                    uniprot.get('dbResNum'), uniprot.get('dbResName'))

                tmp_tup += (pdb.get('dbSource'), pdb.get('dbAccessionId'), pdb.get('dbChainId'), \
                            pdb.get('dbResNum'), pdb.get('dbResName'))

                final.append(tmp_tup)

            elif (self.src_db == 'UniProt') and (lambda_eval['UniProt']()):
                tmp_tup = (uniprot.get('dbSource'), uniprot.get('dbAccessionId'), \
                           uniprot.get('dbResNum'), uniprot.get('dbResName'))
                tmp_tup += ('PDB', pdb_id, None, None, None) if pdb is None else \
                    (pdb.get('dbSource'), pdb.get('dbAccessionId'), pdb.get('dbChainId'), \
                     pdb.get('dbResNum'), pdb.get('dbResName'))

                final.append(tmp_tup)

        if len(final) == 0:
            warnings.warn(
                (f"The given residue position(s), i.e., {query_res_positions} are not present"
                 f" in the {pdb_id} PDB structure."),
                 UserWarning)
        return final


    def __str__(self):
        return f'Residue Mapping started for {self.res_pos} from {self.src_id}'
