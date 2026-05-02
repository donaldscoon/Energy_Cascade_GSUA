# Global Sensitivity and Uncertaintity Analysis of Energy Cascade(s)
This collection of scripts is designed to run global sensitivity and uncertaintity anlaysis (GSUA) on distinct versions of the Energy Cascade (EC) Model.

## The Models
In general the EC's calculate the amount of light intercepted by the canopy and feds that information into a transpiration or biomass pathway. The transpiration pathway calculates in order gross photoysnthesis, net photosynthesis, stomatal conductance, canopy conductance and lastly transpiration. The biomass pathway calculates carbon gain, then daily carbon gain, then total crop biomass and lastly edible biomass. 

There are four seperate versions that follow this framework generally, but have difference in processes and calculations. 

**Volks et. al. Energy Cascade (EC)**
> Volk, T.; Bugbee, B.; Wheeler, R.M. An Approach to Crop Modeling with the Energy Cascade. Life Support Biosph Sci 1995, 1, 119–127.

**Cavazzoni et. al. Modified Energy Cascade (CAV)**
> Cavazzoni, J. Using Explanatory Crop Models to Develop Simple Tools for Advanced Life Support System Studies. Advances in Space Research 2004, 34, 1528–1538, doi:10.1016/j.asr.2003.02.073.

**Boscheri et. al. Modified Energy Cascade (BOS)**
> Boscheri, G.; Kacira, M.; Patterson, L.; Giacomelli, G.; Sadler, P.; Furfaro, R.; Lobascio, C.; Lamantea, M.; Grizzaffi, L. Modified Energy Cascade Model Adapted for a Multicrop Lunar Greenhouse Prototype. Advances in Space Research 2012, 50, 941–951, doi:10.1016/j.asr.2012.05.025.

**Amitrano et. al. Modified Energy Cascade (AMI)**
> Amitrano, C.; Chirico, G.B.; De Pascale, S.; Rouphael, Y.; De Micco, V. Crop Management in Controlled Environment Agriculture (CEA) Systems Using Predictive Mathematical Models. Sensors 2020, 20, 3110, doi:10.3390/s20113110.

These are often reffered to in the scripts with an abbreviation of CAV, BOS, AMI, or EC. They are reproduced as close to the original publications as possible in the scripts `MEC_AMI_GSUA.py`, `MEC_BOS_GSUA.py`, `MEC_CAV_GSUA.py` and `EC_GSUA.py`. 

## The GSUA workflow

`Naming_function.py`

Used to set the user paths, manage labels of inputs and outputs and most criticallly, define the GSUA. 

`sobol_sampling.py`

Used to create the a set of model inputs and parameters to be run for the GSUA.

`HPC_{model-abbreviation}.sh`

This collection of scripts, one for every model, is used to submit a slurm request to a HPC and subsequently run the given simulations utilizing parallelization. For example, the CAV .sh file requests 15 nodes of the HPC to each run 28 tasks, with a single CPU per task. This results in the workload being spread out across 420 CPUs.

`parallel_{model-abbreviation}.py`

These files contain framework for parsing the inputs files genereated by sobol sampling row by row, which are then divided across the available computing resources for running the simulations. Each timestep of every simulation will be printed to the console and saved as a row in a dataframe, which are collected and saved in the file `simulation_results.txt`

`HPC_processing.py` 

This file contains some helpful regex commands for the cleaning of the data files and a method to extract the final timestep from each simulation. This is needed for further processing and analysis.

`analysis_{model-abbreviation}.py`

Each of these files uses the processed HPC simulation data and the specified problem to calculate the elementary effects, and sobol sensitivity indices. The results are saved to .csv files.

`sobol_ST_stacked.py`

This file prepares the data from each model version for charting and creates the horizontal stacked bars used in creating the publication figures. 

## Environment Considerations 
The file `mec.yml` contains all the dependancies and version numbers required to run these scripts in a python python environment. This .yml was used to duplicate the local environment where the scripts were developed and create the environment within the HPC using conda for running this GSUA.

## Pubication Data
Data such as the original input files, simulation results and analysis are stored in a Zenodo repository at doi: 10.5281/zenodo.17307295

The accompanying manuscript can be cited as 
> Donald Coon, Chiara Amitrano, Bruce Bugbee, Ziynet Boz, Ying Zhang, Gerardo H Nunez, Melanie Correll, Rafael Muñoz-Carpena, Ana Martin-Ryals, Performance and Sensitivity of the Energy Cascade Models for Lettuce Production in Bioregenerative Life Support Systems, in silico Plants, 2026;, diag011, https://doi.org/10.1093/insilicoplants/diag011
