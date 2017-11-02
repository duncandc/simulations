#load packages
from __future__ import print_function, division

import numpy as np
import re
import sys
import os

def main():
    
    from astropy.io import ascii
    table_1 = ascii.read("sha1sums.txt", data_start=0, names=['sum','filename']) 
    
    from astropy.io import ascii
    table_2 = ascii.read("sha1sums_post_download.txt", data_start=0, names=['filename','sum']) 
    
    N = len(table_1)
    for i in range(0,N):
        is_a_match = (table_1['sum'][i]==table_2['sum'][i])
        print(table_1['filename'][i], is_a_match)
        if is_a_match==False: print('shasum does not match')
    
if __name__ == '__main__':
    main()
