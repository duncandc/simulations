"""
process particle tables for the Bolshoi simulation
"""

#load packages
from __future__ import print_function, division

import numpy as np
import sys
import re
from astropy.table import Table

from halotools import sim_manager
from halotools.mock_observables.pair_counters import pairwise_distance_3d

base_save_dir = '/Volumes/burt/processed_catalogues/'

def main():
    
    #set the ascii file to process
    filepath = '../particles/'
    if len(sys.argv)>1:
        filename = sys.argv[1]
    else:
        #filename = 'bolshoi_ptcls_0.0001.dat'
        filename = 'bolshoi_ptcls_0.01.dat'
        
    
    sample_rate = float(re.findall(r"[-+]?\d*\.\d+|\d+",filename)[0])
    
    #which version of the halo catalogue will this be matched to?
    version = 'custom'
    
    #set the location and filename of the reduced catalogue
    savepath = base_save_dir + 'Bolshoi/'
    savename = filename[:-4] + '_' + version + '.hdf5'
    
    #define columns
    cols = {'particleId': (1, 'i8'),
            'x':          (2, 'f4'),
            'y':          (3, 'f4'),
            'z':          (4, 'f4'),
            'vx':         (5, 'f4'),
            'vy':         (6, 'f4'),
            'vz':         (7, 'f4')
            }
    
    #read in table
    reader = sim_manager.TabularAsciiReader(filepath+filename, cols, header_char='"') 
    ptcl_table = Table(reader.read_ascii()) 
    print('number of particles: ', len(ptcl_table))
    
    #open halo catalogue
    simname = 'bolshoi_250'
    redshift = 0.0
    halo_finder = 'Rockstar'
    halocat = sim_manager.CachedHaloCatalog(simname=simname, redshift=redshift,
                                            version_name=version, halo_finder=halo_finder)
    halo_table = halocat.halo_table
    
    #define host haloes
    host = (halo_table['halo_upid']==-1)
    
    #keep only host haloes
    halo_table = halo_table[host]
    print('number of host haloes: ', len(halo_table))
    
    #maximum radius to search for particles from the center of each host halo
    r_max = halo_table['halo_rvir']
    
    #define coordinate arrays
    halo_coords = np.vstack((halo_table['halo_x'],
                             halo_table['halo_y'],
                             halo_table['halo_z'])).T
    ptcl_coords = np.vstack((ptcl_table['x'],
                             ptcl_table['y'],
                             ptcl_table['z'])).T
    
    #search for host haloes for particles
    print("searching for host haloes of particles...")
    d_matrix = pairwise_distance_3d(halo_coords, ptcl_coords, r_max, period=halocat.Lbox)
    d_matrix = d_matrix.tocsc()
    print("done.")
    
    #get indices of host haloes and particles that are matched.
    halo_inds, ptcl_inds = d_matrix.nonzero()
    
    #how many haloes have no associated particles?
    unq_halo_ids = np.unique(halo_table['halo_id'][halo_inds])
    mask = np.in1d(halo_table['halo_id'],unq_halo_ids)
    N_w_ptcls = np.sum(mask)
    N_haloes = len(halo_table)
    print("fraction of haloes with >=1 particle found: ", 1.0*N_w_ptcls/N_haloes)
    
    #add host halo ids, index, and host-centric radius to particle table
    ptcl_table['halo_id'] = np.zeros(len(ptcl_table), dtype='int')-1
    ptcl_table['halo_id'][ptcl_inds] = halo_table['halo_id'][halo_inds]
    ptcl_table['halo_index'] = np.zeros(len(ptcl_table), dtype='int')-1
    ptcl_table['halo_index'][ptcl_inds] = halo_inds
    ptcl_table['r'] = np.zeros(len(ptcl_table), dtype='float')-1
    ptcl_table['r'][ptcl_inds] = d_matrix.data
    
    #save particle catalogue
    redshift = halocat.redshift
    Lbox = halocat.Lbox
    particle_mass = halocat.particle_mass
    halo_finder = halocat.halo_finder
    num_ptcls = len(ptcl_table)
    
    d = {key: np.array(ptcl_table[key]) for key in ptcl_table.keys()}
    ptcl_catalog = sim_manager.UserSuppliedPtclCatalog(redshift = redshift,
                                                       Lbox = Lbox,
                                                       particle_mass = particle_mass,
                                                       halo_finder = halo_finder,
                                                       **d)
    
    simname = halocat.simname
    version = str(sample_rate)
    processing_notes = str(sample_rate * 100) + '% of particles'
    ptcl_catalog.add_ptclcat_to_cache(savepath + savename, simname,
                                      version_name=version,
                                      processing_notes=processing_notes,
                                      overwrite=True) 
    
    
if __name__ == '__main__':
    main()