import os
from halotools import sim_manager
import sys

def main():
    
    with open('halocat_list.txt', 'rU') as in_file:
        filenames = in_file.read().split('\n')
    
    abs_path_to_hdf5_file = os.path.dirname(os.path.realpath(__file__))+'/'
    
    for filename in filenames:
        print(abs_path_to_hdf5_file + filename)     
        halocat = sim_manager.CachedHaloCatalog(fname = abs_path_to_hdf5_file + filename, update_cached_fname = True) 
        
if __name__ == '__main__':
    main()