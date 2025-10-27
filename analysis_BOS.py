"""
Boscheri et. al. MEC GSUA Analysis

Author: Donald Coon
Date: January 2025

Description: 
This script automates the process of analyzing the elementary effects and 
sensitivity indices of the Boscheri et al model.

Citation:
    Iwanaga, T., Usher, W., & Herman, J. (2022). Toward SALib 2.0: Advancing 
    the accessibility and interpretability of global sensitivity analyses. 
    Socio-Environmental Systems Modelling, 4, 18155. doi:10.18174/sesmo.18155
    
    Herman, J. and Usher, W. (2017) SALib: An open-source Python library for
    sensitivity analysis. Journal of Open Source Software, 2(9). 
    doi:10.21105/joss.00097

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
from SALib.analyze import morris
from SALib import ProblemSpec
from SALib.sample import morris
import SALib
import numpy as np
import pandas as pd
import naming_function

GSUA_type = 'BOS_expanded' # Artifact of development
gen_path, indiv_path, structure_path, AMI_BLUE_PATH, BOS_BLUE_PATH, BOS_BLUE_PATH = naming_function.path_names()
df_AMI_sims_label, df_BOS_sims_label, df_CAV_sims_label = naming_function.df_labels()

inputs = naming_function.mec_input_names(GSUA_type)
outputs = naming_function.mec_output_names()
models = naming_function.model_names()

sim_file = f'{indiv_path}/GSUA_BOS_out/data/BOS_simulations_LL.txt'
input_file = f'{indiv_path}/GSUA_BOS_out/data/BOS_EXP_parameters.txt'

# Names of the columns in the simulation results file
names = ['SIM_NUM','Timestep','H','diurnal','A','CQY','CUE_24','DCG',
         'CGR','DWCGR','TCB','TEB','VP_SAT','VP_AIR','VPD','P_NET','P_GROSS',
         'DOP','DOC','g_S','g_A','g_C','DTR','DCO2C','DCO2P','DNC','DWC',
         'T_LIGHT','T_DARK','RH','CO2','PPFD','P_ATM','BCF','XFRT','OPF',
         'A_MAX','t_E','CQY_MIN','CUE_MIN','CUE_MAX','D_PG','n','DRY_FR',
         'NC_FR','ta_c2','ta_c3','ta_c5','ta_c7','ta_c9','ta_c11','cqy_max_c7',
         'cqy_max_c8','cqy_max_c9','cqy_max_c12','cqy_max_c18','cqy_max_c19'
         ]    

# Set the problem specifications
sp = naming_function.prob_spec(GSUA_type, inputs)

model_short_name = 'BOS'
ST_S1_Label, S2_label = naming_function.sobol_EE_labels(GSUA_type)

# Create dataframe of the simulation results
df_BOS_sims = pd.read_csv(f'{sim_file}', names=names, delim_whitespace=True)

X = np.loadtxt(f'{input_file}')
X_df = pd.read_csv(f'{input_file}', names= ST_S1_Label, sep=' ')

# Define the number of levels resulting from SOBOL Sampling for EE analysis
N = X_df['H'].nunique() # N = number of levels resulting from SOBOL Sampling

# Create and label dataframes for the results
sobol_ST_out_df = pd.DataFrame({'Index': ST_S1_Label})
sobol_ST_out_df.set_index('Index')

sobol_S1_out_df = pd.DataFrame({'Index': ST_S1_Label})
sobol_S1_out_df.set_index('Index')

sobol_S2_out_df = pd.DataFrame({'Index': S2_label})
sobol_S2_out_df.set_index('Index')

EE_out_df = pd.DataFrame({'Index': ST_S1_Label})
EE_out_df.set_index('Index')
print(f'Data Loaded. Beginning Analysis')

# Iterate through model outputs analyzing each
for output in outputs:
    name = output[0]
    output_long_name = output[1]

    Y = df_BOS_sims[f'{name}'].values

    # Conduct the Sobol and Elementary Effects analysis using SALib
    sp.set_results(Y)
    sp.analyze_sobol()
    EE = SALib.analyze.morris.analyze(sp, X, Y, conf_level=0.95, num_levels=N) # analyzes the Elementary effects for each models ouput

    # EE results
    mu_output_key = f'{model_short_name}_{name}_mu'
    mu_star_output_key = f'{model_short_name}_{name}_mu_star'
    mu_star_conf_output_key = f'{model_short_name}_{name}__mu_star_conf'
    sigma_output_key = f'{model_short_name}_{name}_sigma'

    EE_out_df[mu_output_key] = EE['mu']
    EE_out_df[mu_star_output_key] = EE['mu_star']
    EE_out_df[mu_star_conf_output_key] = EE['mu_star_conf']
    EE_out_df[sigma_output_key] = EE['sigma']

    # First Order Results
    S1_output_key = f'{name}_S1'
    S1_CONF_output_key = f'{name}_S1_conf'
    sobol_S1_out_df[S1_output_key] = sp.analysis['S1'].flatten().tolist()
    sobol_S1_out_df[S1_CONF_output_key] = sp.analysis['S1_conf'].flatten().tolist()

    # Second Order Results
    S2_output_key = f'{name}_S2'
    S2_CONF_output_key = f'{name}_S2_conf'
    sobol_S2_out_df[S2_output_key] = sp.analysis['S2'].flatten().tolist()
    sobol_S2_out_df[S2_CONF_output_key] = sp.analysis['S2_conf'].flatten().tolist()

    # Total Order Results
    ST_output_key = f'{name}_ST'
    ST_CONF_output_key = f'{name}_ST_conf'
    sobol_ST_out_df[ST_output_key] = sp.analysis['ST'].flatten().tolist()
    sobol_ST_out_df[ST_CONF_output_key] = sp.analysis['ST_conf'].flatten().tolist()

    print(f'analysis of {name} completed')

# # # Saving all of these to CSV's
EE_out_df.to_csv(f'{indiv_path}/GSUA_BOS_out/data/EE_out.csv', index=False)
sobol_S1_out_df.to_csv(f'{indiv_path}/GSUA_BOS_out/data/BOS_sobol_S1_out.csv', index=False) # exports entire final data frame to a CSV
sobol_S2_out_df.to_csv(f'{indiv_path}/GSUA_BOS_out/data/BOS_sobol_S2_out.csv', index=False) # exports entire final data frame to a CSV
sobol_ST_out_df.to_csv(f'{indiv_path}/GSUA_BOS_out/data/BOS_sobol_ST_out.csv', index=False) # exports entire final data frame to a CSV
