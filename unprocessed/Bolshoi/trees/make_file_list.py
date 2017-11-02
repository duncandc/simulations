from __future__ import (division, print_function, absolute_import)

def main():

    f = open('file_list.txt','w')
    for i in range(0,5):
        for j in range(0,5):
            for k in range(0,5):
                f.write('tree_'+str(i)+'_'+str(j)+'_'+str(k)+'.dat.gz' + '\n')
    f.close()
    
    
if __name__ == '__main__':
    main()