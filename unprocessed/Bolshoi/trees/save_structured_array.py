""" Module storing functions used to store a Numpy structured array on disk
as a set of binaries with standardized filenames and subdirectory locations.
"""
import os
import numpy as np
from filename_utils import _binary_fname_from_structured_arr_column


def store_structured_array_columns(arr, parent_dirname, columns_to_save='all'):
    """ Function stores the desired columns of a structured array on disk.

    Parameters
    ----------
    arr : array
        Numpy structured array

    parent_dirname : string
        Root directory where the data should be stored

    columns_to_save : sequence of strings, optional
        List of column names that will be saved to disk. Default argument 'all'
        will store all columns.
    """
    dt = arr.dtype
    if columns_to_save == 'all':
        columns_to_save = dt.names
    for colname in columns_to_save:
        msg = "Column name ``{0}`` does not appear in input array".format(colname)
        assert colname in dt.names, msg
        output_dirname = os.path.join(parent_dirname, colname)
        try:
            os.makedirs(output_dirname)
        except OSError:
            pass
        output_fname = os.path.join(output_dirname,
            _binary_fname_from_structured_arr_column(arr, colname))
        np.save(output_fname, arr[colname])


def store_new_trunk_indices_array(scale_factor_array, parent_dirname):
    """
    """
    idx_new_trunks = np.where(scale_factor_array == scale_factor_array.max())[0].astype('i8')
    basename = 'new_trunk_indices_data_' + str(idx_new_trunks.dtype.type.__name__)
    output_fname = os.path.join(parent_dirname, basename)
    try:
        os.makedirs(parent_dirname)
    except OSError:
        pass
    np.save(output_fname, idx_new_trunks)
