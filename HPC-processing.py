"""
MEC-HPC-Processing

Author: Donald Coon
Date: January 2025

Description: 
Clean input data and extract specific simulation timestep from
a simulation results file. The cleaned and filtered data is written to an output file.

Output:
The script will produce a new file with the filtered data at the specified output path.

Variables:
- input_file_path: str, path to the input file containing simulation results.
- output_file_path: str, path to the output file where filtered results will be saved.
- timestep: int, target timestep to filter from the input data.

Example usage:
    # Use the following shell commands in the terminal to clean the input file prior to running this script
    sed -i '1d' input.txt
    sed -i 's/"//g' input.txt

    # Run this in your python environment
    python HPC-processing.py

Note: 
This script may not be neccessary depending on your HPC pipeline/formatting

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

import naming_function

gen_path, indiv_path, _, _, _, _ = naming_function.path_names()

# use a shell terminal to clean the data for future steps with the following commands
# sed -i '1d' input.txt to remove the first line
# sed -i 's/"//g' input.txt to remove the quotation marks

# Define the input and output file paths do this for each model.
input_file_path = f'{indiv_path}/GSUA_EC_out/data/simulation_results.txt'  
output_file_path = f'{indiv_path}/GSUA_EC_out/data/EC_simulations_LL.txt'  # Replace with your desired output file path

# Define the target integer value of the desired timestep to pull from each simulation
timestep = 35

# Opent the file 
with open(input_file_path, 'r') as file, open(output_file_path, 'w') as outfile:
    # read a single timestep of a single simulation
    for line in file:
        # processing the line into a slicable form for the following logic
        columns = line.strip().split() 
        if int(columns[1]) == timestep:
            # append the line to the output file
            outfile.write(line) 
            # print(line)

print("Ken would be pleased")