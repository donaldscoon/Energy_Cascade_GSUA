#!/bin/bash

# HPC for Boscheri Model

# Author: Donald Coon
# Date: January, 2025

# Description: Used to submit and run parallel simulations of the Boscheri et. al. model
# on the University of Florida HyperGator. May differ from between HPCs and slurm managers

# License: None
#SBATCH --job-name=mec_bos
#SBATCH --account=XXXX
#SBATCH --qos=XXXX
#SBATCH --output=mec_bos_%j.out
#SBATCH --error=mec_bos_%j.err
#SBATCH --nodes=15
#SBATCH --ntasks-per-node=28
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=8500 # default unit = MB
#SBATCH --time=100:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=XXXX

pwd; hostname; date

module load conda
conda activate mec

python parallel_bos.py

## echo "Job Finished (this doesn't guarantee completion)"

date

