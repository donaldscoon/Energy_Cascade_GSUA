"""
MEC GSUA Sampling Function

Author: Donald Coon
Date: January 2025

Description: 
This script performs Sobol sampling for various types of General Sensitivity and Uncertainty Analysis (GSUA)
and stores the sample parameters to specified paths. Additionally, it ensures the necessary paths and files 
exist for saving the generated samples.

Notes:
Path names are and problem spec are assigned in naming_function.py

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

from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib import ProblemSpec

import numpy as np
import pandas as pd
import warnings
import naming_function


warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UserWarning)

gen_path, indiv_path, structure_path, AMI_BLUE_PATH, BOS_BLUE_PATH, CAV_BLUE_PATH = naming_function.path_names()
_, EC_BLUE_PATH, _ = naming_function.EC_info()

sobol_tests = [
         ["ST", "Total Order"], 
         ["S1", "1st Order"], 
         ["S2", "2nd Order"]
         ]

elinewidth, capsize, capthick = naming_function.conf_bars()

def SAMPLE(GSUA_type, inputs):
    """
    Generate and save Sobol samples for the specified GSUA type.

    This function establishes a problem specification, generates Sobol samples,
    and saves them to the pre-defined paths based on the GSUA type.

    Parameters
    ----------
    GSUA_type : str
        Specifies the type of GSUA being performed.
    inputs : any
        Additional input parameters, currently not used.

    Notes
    -----
    Ensures that the necessary file paths exist before saving the samples.
    """

    sp = naming_function.prob_spec(GSUA_type, inputs)
    multiplier = 2**12

    if GSUA_type == 'CAV_expanded':
        sample_path = f'{CAV_BLUE_PATH}/CAV_EXP_parameters.txt'
        naming_function.ensure_file_exists(sample_path)
        param_values = sp.sample_sobol(multiplier, calc_second_order=True)
        np.savetxt(f'{CAV_BLUE_PATH}/CAV_EXP_parameters.txt', sp.samples)
    elif GSUA_type == 'BOS_expanded':
        sample_path = f'{BOS_BLUE_PATH}/BOS_EXP_parameters.txt'
        naming_function.ensure_file_exists(sample_path)
        param_values = sp.sample_sobol(multiplier, calc_second_order=True)
        np.savetxt(f'{BOS_BLUE_PATH}/BOS_EXP_parameters.txt', sp.samples)
    elif GSUA_type == 'AMI_expanded':
        sample_path = f'{AMI_BLUE_PATH}/AMI_EXP_parameters.txt'
        naming_function.ensure_file_exists(sample_path)
        param_values = sp.sample_sobol(multiplier, calc_second_order=True)
        np.savetxt(f'{AMI_BLUE_PATH}/AMI_EXP_parameters.txt', sp.samples)
    elif GSUA_type == "Energy_Cascade":
        sample_path = f'{EC_BLUE_PATH}/EC_EXP_parameters.txt'
        naming_function.ensure_file_exists(sample_path)
        param_values = sp.sample_sobol(multiplier, calc_second_order=True)
        np.savetxt(f'{EC_BLUE_PATH}/EC_EXP_parameters.txt', sp.samples)
