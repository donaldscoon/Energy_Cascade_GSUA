#!/bin/bash

# HPC for Amitrano Model

# Author: Donald Coon
# Date: January 2025

# Description: Used to submit and run parallel simulations of the Amitrano et. al. model
# on the University of Florida HyperGator. May differ from between HPCs and slurm managers

# License: None

#SBATCH --job-name=mec_ami
#SBATCH --account=XXXX
#SBATCH --qos=XXXX
#SBATCH --output=mec_ami_%j.out
#SBATCH --error=mec_ami_%j.err
#SBATCH --nodes=15
#SBATCH --ntasks-per-node=28
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1000 # default unit = MB
#SBATCH --time=05:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=XXXX

pwd; hostname; date

module load conda
conda activate mec

python parallel_ami.py

## echo "Job Finished (this doesn't guarantee completion)"

date

