#!/bin/bash

N=8

i=0
j=0
k=0
t=001

while [ $i -lt $N ]
do
	  j=0
    while [ $j -lt $N ]
    do
    	  k=0
        while [ $k -lt $N ]
        do
            n=$(printf %03d $t)
            orig_fname="subvol_"$n".csv";
            new_fname="subvol_""$i""_""$j""_""$k"".csv";
            mv $orig_fname $new_fname
            k=$(( k+1 ))
            t=$(( t+1 ))
        done
        j=$(( j+1 ))
    done
    i=$(( i+1 ))
done 
