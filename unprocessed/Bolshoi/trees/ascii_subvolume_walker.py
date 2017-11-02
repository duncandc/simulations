""" Module containing the generator used to walk full rockstar merger trees and
return the main progenitor histories.
"""
import gzip


def _compression_safe_opener(fname):
    """ Determine whether to use *open* or *gzip.open* to read
    the input file, depending on whether or not the file is compressed.
    """
    f = gzip.open(fname, 'r')
    try:
        f.read(1)
        opener = gzip.open
    except IOError:
        opener = open
    finally:
        f.close()
    return opener


def mmp_row_generator(tree_fname, mmp_col_index, desc_id_col_index, halo_id_col_index,
        *colnums_to_yield):
    """ Given an input hlist ASCII file, yield the desired columns of all rows
    storing the main progenitors in the file.
    Parameters
    ----------
    tree_fname : string
        Absolute path to the ascii file storing the rockstar merger tree information
        of a single subvolume.
    mmp_col_index : int
        Column number where the ``mmp`` appears (the first column has index 0).
    desc_id_col_index : int
        Column number where the ``desc_id`` appears.
    halo_id_col_index : int
        Column number where the ``halo_id`` appears.
    *colnums_to_yield : sequence of integers
        Determines which columns the generator will yield.
    Returns
    -------
    string_data : tuple
        Tuple storing a row of mmp data. Each column of the yielded row
        has its data stored as a string.
    """
    opener = _compression_safe_opener(tree_fname)
    with opener(tree_fname, 'r') as f:

        # Skip the header, extracting num_trees
        while True:
            raw_header_line = next(f)
            if raw_header_line[0] != '#':
                break

        # Iterate over remaining ascii lines
        while True:
            try:
                raw_line = next(f)
                if raw_line[0] == '#':
                    current_trunk_id = raw_line.strip().split()[1]
                else:
                    list_of_strings = raw_line.strip().split()

                    # Extract the 3 columns we'll use to identify the trunk
                    mmp = list_of_strings[mmp_col_index]
                    desc_id = list_of_strings[desc_id_col_index]
                    halo_id = list_of_strings[halo_id_col_index]

                    # The row is on the trunk if the desc_id points to the previous trunk id
                    # or if we have just started a new trunk
                    yield_current_line = ((mmp == '1') & (desc_id == current_trunk_id) |
                        (halo_id == current_trunk_id))

                    if yield_current_line:
                        string_data = tuple(list_of_strings[idx] for idx in colnums_to_yield)
                        current_trunk_id = halo_id
                        yield string_data

            except StopIteration:
                break