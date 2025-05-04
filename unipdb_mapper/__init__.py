 #!/usr/bin/env python3
"""
unipdb_mapper: A Python package to map residues between UniProt and PDB databases.
"""

__author__ = 'Hrishikesh DHONDGE'
__version__ = '1.0.0'

import warnings
from .utilities import *
from .residue_mapper import ResidueMapper
from .id_mapper import IDMapper

def custom_warning(message, category, _filename=None, _lineno=None, _file=None, _line=None):
    """
    Custom warnings so it won't show specific filename and line numbers in package
    """
    print(f"{category.__name__}: {message}")

warnings.showwarning = custom_warning
