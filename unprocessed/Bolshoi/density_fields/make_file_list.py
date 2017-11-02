from __future__ import (division, print_function, absolute_import)

def main():
    
    #make file list
    f = open('file_list.txt','w')
    
    from astropy.table import Table
    t = Table.read('snapsum.csv')
    print(t)
    
    for i in range(0,len(t)):
        snap = t['snapnum'][i]
        if snap >= 100:
            fname = 'dens256_'+str(snap)+'.csv' + '\n'
        elif (snap < 100) & (snap >= 10):
            fname = 'dens256_0'+str(snap)+'.csv' + '\n'
        elif snap < 10:
            fname = 'dens256_00'+str(snap)+'.csv' + '\n'
        f.write(fname)
    f.close()
    
    #check to see if all files are there
    import os  
    for i in range(0,len(t)):
        snap = t['snapnum'][i]
        if snap >= 100:
            fname = 'dens256_'+str(snap)+'.csv'
        elif (snap < 100) & (snap >= 10):
            fname = 'dens256_0'+str(snap)+'.csv'
        elif snap < 10:
            fname = 'dens256_00'+str(snap)+'.csv'
        print(fname, os.path.isfile('./'+fname))
    
    
if __name__ == '__main__':
    main()