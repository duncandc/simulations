#Duncan Campbell
#March 2017
#Yale University

#load packages
from __future__ import print_function, division
import numpy as np
import string
import os
import fnmatch

"""
make an array that stores the sub-volume and index of each halo
"""

def main():
    
    result = id_generator('./', ndivs=5)
    np.save('./halo_id_index.npy', result)
    
def id_generator(tree_directory, ndivs=5):
    """
    Find the peak halo mass.
    """
    dir_names = list(yield_subvol_directories(tree_directory, ndivs))
    
    result = np.zeros((0,4))
    for i,name in enumerate(dir_names):
        
        #load arrays
        fnames = yield_trunk_array_fname(name, ['halo_id'])
        inds = np.load(fnames[0])
        halo_id = np.load(fnames[1])
        
        print("on subvolume {0}/{1} with {2} haloes.".format(i+1, ndivs**3, len(inds)))
        
        sub_result = np.zeros((len(inds),4))
        j = 0
        for ifirst, ilast in zip(inds[:-1], inds[1:]):
            sub_result[j,0] = halo_id[ifirst]
            sub_result[j,1] = i
            sub_result[j,2] = ifirst
            sub_result[j,3] = ilast
            j+=1
            
        #free up memory
        inds = 0.0
        result = np.vstack((result,sub_result))
    return result

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
        i //= n

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return int(''.join(digits))


def tree_subvol_substring_from_int(i, n):
    """ 
    From any non-negative integer i, and n subdivisions per dimension,
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

def yield_subvol_directories(trunks_dirname, ndivs):
    """
    """
    for i in range(0,ndivs**3):
        yield os.path.join(trunks_dirname,'subvol_'+tree_subvol_substring_from_int(i, ndivs))

def yield_trunk_array_fname(trunks_dirname, haloprop_names):
    """
    """
    fnames = []
    fnames.append(os.path.join(trunks_dirname,'new_trunk_indices_data_int64.npy'))
    for name in haloprop_names:
        fname = os.path.join(trunks_dirname,name)
        for file in os.listdir(fname):
            fnames.append(os.path.join(fname,file))
    return fnames


if __name__ == '__main__':
    main()