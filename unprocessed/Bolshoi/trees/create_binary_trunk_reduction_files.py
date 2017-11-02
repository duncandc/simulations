""" Executable script reading hlist ascii data and producing a collection
of Numpy binaries with standardized filenames and directory locations.
"""
import argparse
import os
from simulation_column_dtype import simulation_column_dtype, sub_dtype
from filename_utils import fname_generator, _binary_fname_from_structured_arr_column
from ascii_subvolume_walker import mmp_row_generator
from time import time
import numpy as np
from save_structured_array import store_structured_array_columns, store_new_trunk_indices_array
from warnings import warn

parser = argparse.ArgumentParser()

parser.add_argument("input_dirname",
    help="Disk location of the input hlist ascii data. "
    "Filenames are assumed to conclude with 'i_j_k.dat'")

parser.add_argument("output_dirname",
    help="Desired directory to store the output Numpy binaries")

parser.add_argument("colnames",
        help="Sequence of names of the columns for which you want to create binaries. "
        "Each string in the sequence must appear somewhere in the first column "
        "of the `tree_column_info_fname` file.",
        nargs='+')

parser.add_argument("-input_hlist_filepat",
    help="Filename pattern used to identify the hlist ascii data "
    "in the input_dirname. Default is `tree_*`",
    default="tree_*")

parser.add_argument("-tree_column_info_fname",
    help="Name of the user-created ascii file "
    "used to infer the dtype of the data stored in the hlist ascii file. "
    "Must at least have ``mmp``, ``desc_id``, ``halo_id`` and ``scale_factor`` as column names."
    "See simulation_column_dtype for example formatting."
    "Default assumes tree hlist files are associated with "
    "simname = `bolplanck`, version_name = `version_0p4`",
    default="bolshoi_columns.dat")


args = parser.parse_args()
try:
    os.makedirs(args.output_dirname)
except OSError:
    pass

hlist_dt = simulation_column_dtype(args.tree_column_info_fname)

assert os.path.isdir(args.input_dirname), "input_dirname is not recognized on disk"

try:
    mmp_col_index = hlist_dt.names.index('mmp')
    desc_id_col_index = hlist_dt.names.index('desc_id')
    halo_id_col_index = hlist_dt.names.index('halo_id')
    assert 'scale_factor' in hlist_dt.names
except (ValueError, AssertionError):
    msg = ("The `tree_column_info_fname` file must at least have columns named \n"
            "``mmp``, ``desc_id``, ``halo_id`` and ``scale_factor``.")
    raise ValueError(msg)

colnames_to_yield = args.colnames
if 'scale_factor' not in colnames_to_yield:
    colnames_to_yield.append('scale_factor')
    warn("Automatically adding ``scale_factor`` to colnames_to_yield")
colnums_to_yield = [hlist_dt.names.index(name) for name in colnames_to_yield]

output_dt = sub_dtype(hlist_dt, args.colnames)

print("\n")
start = time()
for tree_fname in fname_generator(args.input_dirname, args.input_hlist_filepat):
    print("...working on {0}".format(os.path.basename(tree_fname)))

    # Uncompress the file if necessary
    was_zipped = False
    try:
        assert tree_fname[-4:] == ".dat", "Input filename must conclude with '.dat'"
    except AssertionError:
        was_zipped = True
        os.system("gunzip -f " + tree_fname)
        tree_fname = tree_fname[:-3]
        assert tree_fname[-4:] == ".dat", "Input filename must conclude with '.dat'"

    # Read the ascii data for the subvolume
    subvolume_data = np.array(list(mmp_row_generator(tree_fname,
        mmp_col_index, desc_id_col_index, halo_id_col_index, *colnums_to_yield)), dtype=output_dt)
    
    #re-zip file if it was zipped initially
    if was_zipped:
        os.system("gzip " + tree_fname)
    
    # Write the data to a Numpy binary
    subvol_output_dirname = os.path.join(args.output_dirname, "subvol_"+tree_fname[-9:-4])
    store_structured_array_columns(subvolume_data, subvol_output_dirname)

    # Save the array storing the indices of the trunks
    scale_factor_array_basename = _binary_fname_from_structured_arr_column(
        subvolume_data, 'scale_factor')+'.npy'
    scale_factor_array_fname = os.path.join(subvol_output_dirname,
            'scale_factor', scale_factor_array_basename)
    scale_factor_array = np.load(scale_factor_array_fname)
    store_new_trunk_indices_array(scale_factor_array, subvol_output_dirname)

end = time()
print("\nTotal runtime = {0:.1f} minutes\n".format((end-start)/60.))
