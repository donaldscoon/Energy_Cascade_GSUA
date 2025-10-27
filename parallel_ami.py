"""
Parallelization of the AMI simulations

Author: Donald Coon
Date: January 2025
Description: 
    This script facilitates the parallel execution of simulations 
    of the Amitrano et. al. Modified Energy Cascade crop model. It was
    designed to be called with a bash script and utilize HPC resources.

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

#!/usr/bin/env python
import os
import pandas as pd
import dask
from dask.delayed import delayed
import subprocess
import multiprocessing as mp
import subprocess
import naming_function
import numpy as np
import json

# add file paths
gen_path, indiv_path, structure_path, AMI_BLUE_PATH, BOS_BLUE_PATH, CAV_BLUE_PATH = naming_function.path_names()

data = np.loadtxt(f'{AMI_BLUE_PATH}AMI_EXP_parameters.txt')

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Add a unique ID column
df.insert(0, 'SIM_NUM', range(1, len(df)+1))

# Convert each row to a dictionary
rows = df.to_dict('records')

def run_simulation(row):
    """Run a single simulation."""
    # Convert params to a format suitable for the simulation script
    params = [
              row['SIM_NUM'], row[0], row[1], row[2], row[3], row[4],
              row[5], row[6], row[7], row[8], row[9], row[10],
              row[11], row[12], row[13], row[14], row[15], row[16],
              row[17], row[18], row[19]
             ]

    # Convert all parameters to strings
    param_strs = list(map(str, params))

    # Call the simulation script with the parameters
    result = subprocess.run(
        ['python', 'MEC_AMI_GSUA.py'] + param_strs,
        capture_output=True, text=True
    )

    # Print the unique identifier and result
    # print(f"Simulation ID: {row['SIM_NUM']}")
    print("Standard Output:\n", result.stdout)
    print("Standard Error:\n", result.stderr)

    # Process the output and return it
    output = result.stdout.strip()
    return output

if __name__ == '__main__':
    # Create a multiprocessing pool
    rows = df.to_dict('records')
    with mp.Pool() as pool:
        # Map the run_simulation function to each row in the DataFrame
        results = pool.map(run_simulation, rows)
        # print(results)

    # Save the results
    output_file = os.path.join(AMI_BLUE_PATH, 'simulation_results.txt')
    results_df = pd.DataFrame(results, columns=['Output'])
    results_df.to_csv(output_file, index=False)
