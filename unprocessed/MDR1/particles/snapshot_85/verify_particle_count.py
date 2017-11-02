#!/usr/bin/env python

from __future__ import print_function, division
import numpy as np 
import os, sys, fnmatch
from astropy.io import ascii

def main():
    
    fnames = []
    if len(sys.argv)==1:
        for file in os.listdir('.'):
            if fnmatch.fnmatch(file, '*_N_*.csv'):
                fnames.append(file)
    else: 
        fnames.append(sys.argv[1])
    
    N = len(fnames)
    print("Number of files:", N)

    I = np.array([i.split('_')[2].split('.')[0] for i in fnames])
    J = np.array([i.split('_')[3].split('.')[0] for i in fnames])
    K = np.array([i.split('_')[4].split('.')[0] for i in fnames])
    
    missing_ptcls = open('files_w_missing_ptcls.txt','w')

    j = 0
    jstart=0
    Ntot=0
    for i in range(0,N):
        fname = 'subvol_'+I[i]+'_'+J[i]+'_'+K[i]+'.csv'
        if j>=jstart:
            N_lines = file_len(fname)
        else:
            N_lines = 0
        
        data = ascii.read('subvol_N_'+I[i]+'_'+J[i]+'_'+K[i]+'.csv')  
        N_ptcls = data['_COUNT_particleId_']
        
        Ntot += N_ptcls[0]
        
        print(i, fname,  N_lines-1, N_ptcls[0], (N_lines-1)==N_ptcls[0], Ntot)
        
        if (j>=jstart) & ((N_lines-1)!=N_ptcls[0]):
             missing_ptcls.write(fname + '\n')

        j=j+1

    missing_ptcls.close()
    
def file_len(fname):
    """
    count the number of lines in a file
    similar to wc -l
    """
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

if __name__ == "__main__":
    main()