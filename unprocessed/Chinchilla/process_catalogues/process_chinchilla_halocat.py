"""
process ROCKSTAR halo catalogues from Bolshoi
"""

#load packages
from __future__ import print_function, division

import numpy as np
import re
import sys

from halotools import sim_manager

base_save_dir = '/Volumes/burt/processed_catalogues/'

def main():
    
    #set the ascii file to process
    filepath = '../halo_catalogues/'
    if len(sys.argv)>1:
        filename = sys.argv[1]
    else:
        filename = 'lb125_hlist_1.00000.list'
    
    box_size = float(re.findall(r"[-+]?\d*\.\d+|\d+",filename)[0])
    scale_factor = float(re.findall(r"[-+]?\d*\.\d+|\d+",filename)[1])
    
    #set some properties
    simname = 'chinchilla_' + str(int(box_size))
    version = 'custom'
    Lbox = box_size
    particle_mass = (1.36*10**8.0) / ((250.0/Lbox)**3) #125 box has smaller particles
    halo_finder='Rockstar'
    
    #set the location and filename of the reduced catalogue
    savepath = base_save_dir+'Chinchilla/'
    savename = filename + '_' + version + '.hdf5'
    
    #extract the scale factor of the snapshot from the filename
    scale_factor = float(re.findall(r"[-+]?\d*\.\d+|\d+",filename)[1])
    redshift = 1.0/scale_factor -1.0
    
    ####
    ####Note that 250 and 125 boxes have different columns!
    ####
    
    if filename == 'lb125_hlist_1.00000.list':
        columns_to_keep_dict = {'halo_id':              (1, 'i8'),
                            'halo_pid':             (5, 'i8'),
                            'halo_upid':            (6, 'i8'),
                            'halo_mvir':            (10, 'f4'),
                            'halo_rvir':            (11, 'f4'),
                            'halo_rs':              (12, 'f4'),
                            'halo_vmax':            (16, 'f4'),
                            'halo_x':               (17, 'f4'),
                            'halo_y':               (18, 'f4'),
                            'halo_z':               (19, 'f4'),
                            'halo_vx':              (20, 'f4'),
                            'halo_vy':              (21, 'f4'),
                            'halo_vz':              (22, 'f4'),
                            'halo_m200b':           (36, 'f4'),
                            'halo_m200c':           (37, 'f4'),
                            'halo_macc':            (56, 'f4'),
                            'halo_mpeak':           (57, 'f4'),
                            'halo_vacc':            (58, 'f4'),
                            'halo_vpeak':           (59, 'f4'),
                            'halo_half_mass_scale': (60, 'f4'),
                            'halo_mpeak_scale':     (66, 'f4'),
                            'halo_acc_scale':       (67, 'f4')
                            }
    
    elif filename == 'lb250_hlist_1.00000.list':
        columns_to_keep_dict = {'halo_id':              (1, 'i8'),
                            'halo_pid':             (5, 'i8'),
                            'halo_upid':            (6, 'i8'),
                            'halo_mvir':            (10, 'f4'),
                            'halo_rvir':            (11, 'f4'),
                            'halo_rs':              (12, 'f4'),
                            'halo_vmax':            (16, 'f4'),
                            'halo_x':               (17, 'f4'),
                            'halo_y':               (18, 'f4'),
                            'halo_z':               (19, 'f4'),
                            'halo_vx':              (20, 'f4'),
                            'halo_vy':              (21, 'f4'),
                            'halo_vz':              (22, 'f4'),
                            'halo_m200b':           (36, 'f4'),
                            'halo_m200c':           (37, 'f4'),
                            'halo_macc':            (54, 'f4'),
                            'halo_mpeak':           (55, 'f4'),
                            'halo_vacc':            (56, 'f4'),
                            'halo_vpeak':           (57, 'f4'),
                            'halo_half_mass_scale': (58, 'f4'),
                            'halo_mpeak_scale':     (64, 'f4'),
                            'halo_acc_scale':       (65, 'f4')
                            }
    
    columns_to_convert_from_kpc_to_mpc = ['halo_rvir','halo_rs']
    
    #apply cuts to catalogue
    row_cut_min_dict = {'halo_mpeak': particle_mass*50}
    processing_notes = ("all halos with halo_mpeak < 50 times the particle mass were \n"
                        "thrown out during the initial catalogue reduction.")
    
    #read in catalogue and save results
    reader = sim_manager.RockstarHlistReader(filepath+filename, columns_to_keep_dict,\
        savepath+savename, simname, halo_finder, redshift, version, Lbox, particle_mass,\
        row_cut_min_dict=row_cut_min_dict, processing_notes=processing_notes,\
        overwrite=True) 
    
    reader.read_halocat(columns_to_convert_from_kpc_to_mpc, write_to_disk = True, update_cache_log = True) 


if __name__ == '__main__':
    main()