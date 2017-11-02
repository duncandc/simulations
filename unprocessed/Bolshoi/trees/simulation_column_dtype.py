""" Module storing function used to determine
the Numpy dtype of Rockstar hlist ascii data.
"""
import numpy as np


def simulation_column_dtype(fname='bolshoi_columns.dat'):
    """ Function returning the Numpy dtype given user-created ascii data that
    places the Rockstar hlist header information into a specific format.
    The specific format is described below; see the ``bolplanck_columns.dat``
    file for a specific example.

    The ascii data should have one row for every column of data in the
    merger tree hlist file. Each row should have two space-separated strings.
    The first string stores the name of the column
    (e.g., 'halo_id' or 'mvir'); column names should only use alphanumeric
    characters, and may not contain spaces or special characters.
    The second string stores the type of data.
    Use 'f4' for float, 'f8' for double, 'i4' for int, and 'i8' for long.

    Parameters
    -----------
    fname : string
        Absolute path to the ascii file providing the formatting information.

    Returns
    -------
    dt : `numpy.dtype`
        Numpy dtype object defining the formatting for the rockstar
        merger tree hlist file.
    """
    data_types = []
    with open(fname, 'r') as f:
        for raw_line in f:
            line = tuple(s for s in raw_line.strip().split())
            data_types.append(line)

    return np.dtype(data_types)


def sub_dtype(dtype, names):
    """
    """
    return np.dtype([(name, dtype[name]) for name in names])


