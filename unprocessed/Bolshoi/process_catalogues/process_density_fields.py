"""
process density fields for Bolshoi from CosmoSim
"""

#load packages
from __future__ import print_function, division

import numpy as np
import re
import sys

from halotools import sim_manager

base_save_dir = '/Volumes/burt/simulations/processed/'

def main():
    
    #set the ascii file to process
    filepath = '../density_fields/'
    if len(sys.argv)>1:
        filename = sys.argv[1]
    else:
        filename = 'dens256_416.csv'
    
    """
    #read ascii file
    import pandas as pd
    data = pd.read_csv(filepath+filename)
    ix = data['ix']
    iy = data['iy']
    iz = data['iz']
    dens = data['dens']
    
    #sort by indices
    sort_inds = np.lexsort((iz, iy, ix))
    
    #put into an astropy table
    from astropy.table import Table
    t = Table([ix[sort_inds], iy[sort_inds], iz[sort_inds], dens[sort_inds]], names=('ix', 'iy', 'iz', 'dens'))
    print(t)
    
    #save in hdf5 format
    filename = filename.split('.')[0]+'.hdf5'
    save_dir = base_save_dir+'Bolshoi/'+'density_fields/'
    t.write(save_dir + filename, path='data', overwrite=True)
    """
    
    #process snapnum file
    from astropy.table import Table
    t = Table.read(filepath + 'snapsum.csv')
    print(t)
    filename = 'snapnum.dat'
    save_dir = base_save_dir+'Bolshoi/'+'density_fields/'
    t.write(save_dir + filename, format='ascii')
    
    

if __name__ == '__main__':
    main()