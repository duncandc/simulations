""" Functions used for generating and interpreting typical filename patterns
used in rockstar hlist analysis.
"""
import string
import os
import fnmatch
import numpy as np


__all__ = ('base_10_signed_int_to_base_n_signed_int', 'tree_subvol_substring_from_int')


def base_10_signed_int_to_base_n_signed_int(i, n):
    digs = string.digits + string.letters

    if i < 0:
        sign = -1
    elif i == 0:
        return digs[0]
    else:
        sign = 1
    i *= sign

    digits = []
    while i:
        digits.append(digs[i % n])
        i /= n

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return int(''.join(digits))


def tree_subvol_substring_from_int(i, n):
    """ From any non-negative integer i, and n subdivisions per dimension,
    return the substring designating the corresponding subvolume.

    For an explicit example, the following (i, n) pairs yield the values below:

    (2, 5) --> '0_0_2'
    (5, 5) --> '0_1_0'
    (24, 5) --> '0_4_4'
    (25, 5) --> '1_0_0'
    """
    error_msg = ("The `tree_subvol_substring_from_int` function "
        "is only intended \nto work with 3d subvolumes "
        "with at most 10 subdivisions per dimension.\n"
        "You selected n = {0} subdivisions, for which there are "
        "at most {1} different subvolumes, \n"
        "exceeding your request for file number i = {2}.".format(n, n**3, i))

    s = str(base_10_signed_int_to_base_n_signed_int(i, n))
    if len(s) == 1:
        return '0_0_'+s
    elif len(s) == 2:
        return '0_'+s[0]+'_'+s[1]
    elif len(s) == 3:
        return '_'.join(s)
    else:
        raise ValueError(error_msg)


def _binary_fname_from_structured_arr_column(arr, colname):
    """ For column  ``colname`` of an input structured array ``arr``,
    use the dtype to create a string that will be used as the basename
    of the file storing a Numpy binary of the data for that column.
    """
    msg = "Column name ``{0}`` does not appear in input array".format(colname)
    assert colname in arr.dtype.names, msg

    type_string = str(arr[colname].dtype.type.__name__)
    return colname + '_data_' + type_string


def fname_generator(input_dirname, filepat):
    """ Yield all the files in ``input_dirname`` with basenames matching
    the specified file pattern.
    """
    for path, dirlist, filelist in os.walk(input_dirname):
        for name in fnmatch.filter(sorted(filelist), filepat):
            yield os.path.join(path, name)
