"""
MEC GSUA Sampling Procedure

Author: Donald Coon
Date: January 2025

Description: 
This script performs Sobol sampling for each of the Energy Cascade models, 
and saves the samples to specified paths to be used later. 

Notes:
Path names are assigned in naming_function.py

License: MIT Liscense

Usage Rights: Redistribution and use in source and binary forms, 
              with or without modification, are permitted provided 
              that the following conditions are met:
              * Redistributions of source code must retain the 
                above copyright notice, this list of conditions 
                and the following disclaimer.
              * Redistributions in binary form must reproduce the 
                above copyright notice, this list of conditions 
                and the following disclaimer in the documentation
                and/or other materials provided with the distribution.
"""


from SALib.analyze import sobol
import SOBOL_SAMPLE
import naming_function

# Assign paths of where to save the sample files.
gen_path, indiv_path, structure_path, AMI_BLUE_PATH, BOS_BLUE_PATH, CAV_BLUE_PATH= naming_function.path_names()
paths = [f'{AMI_BLUE_PATH}', f'{BOS_BLUE_PATH}', f'{CAV_BLUE_PATH}']

# Sample files to be created
GSUA_type = ['AMI_expanded', 'BOS_expanded', 'CAV_expanded']

# iterate through the different GSUA types, creating their samples
for type, path in zip(GSUA_type, paths):
	inputs = naming_function.mec_input_names(type)
	SOBOL_SAMPLE.SAMPLE(type, inputs)
	print(f'{type} samples saved to {path}')

# Sobol sampling procedure for the Volk EC model
gen_path, EC_BLUE_PATH, GSUA_type = naming_function.EC_info()
inputs = naming_function.mec_input_names(GSUA_type)
SOBOL_SAMPLE.SAMPLE(GSUA_type, inputs)
print(f'{GSUA_type} samples saved to {EC_BLUE_PATH}')
