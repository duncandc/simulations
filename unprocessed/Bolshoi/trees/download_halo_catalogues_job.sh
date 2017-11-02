#!/bin/bash 
#PBS -N download_bolshoi_trees-03-27-17
#PBS -q fas_normal
#PBS -l nodes=1:ppn=1,mem=8gb
#PBS -l walltime=24:00:00
#PBS -j oe
#PBS -m abe
#PBS -M duncan.campbell@yale.edu

# Switch to the working directory; by default PBS launches processes
# from your home directory.
echo Working directory is $PBS_O_WORKDIR
cd /home/fas/padmanabhan/dac29/scratch/data/Bolshoi/trees

echo Running on host `hostname`
echo Time is `date`
echo Directory is `pwd`

# Run your job
./download_halo_catalogues_reverse.sh
