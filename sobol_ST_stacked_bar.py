"""
MEC GSUA Sampling Procedure

Author: Donald Coon
Date: January 2025

Description: 
This script processes and prepares Sobol data for visualization, and generates bar plots to show the 
percentage of output variance attributed to various inputs. Additionally, it creates a master legend 
combining color and label information for all models.

Examples:
---------
To run this script, simply execute it in an environment where the `naming_function` module is available.

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


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import naming_function
import matplotlib.patches as mpatches


def process_and_prepare_bars(S1_df, ST_df, output, variables=[], sobol_cutoff=0):
    """
    Processes Sobol sensitivity analysis results and prepares data for bar plots.

    This function takes Sobol sensitivity analysis results from S1 and ST dataframes,
    normalizes, and filters them. It returns a pandas DataFrame with the percentage 
    contributions of the total order (ST), first order (S1), and interaction effects 
    for each input variable.

    Parameters
    ----------
    S1_df : pandas.DataFrame
        DataFrame containing first-order Sobol indices.
    ST_df : pandas.DataFrame
        DataFrame containing total-order Sobol indices.
    output : str
        The name of the output variable for which Sobol indices are processed.
    variables : list, optional
        A list of input variable names. Default is an empty list.
    sobol_cutoff : float, optional
        Threshold for filtering out small Sobol indices. Values below this threshold 
        are set to zero. Default is 0.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the percentage contributions of the total-order (ST), 
        first-order (S1), and interaction effects for each input variable. 
        The DataFrame has columns: 'inputs', 'ST', 'S1', 'interactions'.

    Notes
    -----
    1. Filters out rows where both ST, S1, and the interaction effect are zero.
    2. Aggregates variables with small ST contributions into an 'Other' category.
    3. Ensures proper sorting and resetting of the index for the final DataFrame.
    """

    if f'{output}_S1' not in S1_df.columns or f'{output}_ST' not in ST_df.columns:
        return pd.DataFrame(columns=['inputs', 'ST', 'S1', 'interactions'])
    
    S1_values = S1_df[f'{output}_S1'].mask(lambda x: x < sobol_cutoff, 0)
    ST_values = ST_df[f'{output}_ST'].mask(lambda x: x < sobol_cutoff, 0)
    sum_ST = ST_values.sum()
    bars = pd.DataFrame({
        'inputs': variables,
        'ST': ((ST_values / sum_ST) * 100).round(2),
        'S1': ((S1_values / sum_ST) * 100).round(2),
        'interactions': ((ST_values - S1_values) / sum_ST * 100).round(2).abs()
    })
    bars = bars.loc[~((bars['interactions'] == 0) & (bars['ST'] == 0) & (bars['S1'] == 0))]

    below_cutoff = bars[bars['ST'] < other_cutoff]
    other_ST_sum = below_cutoff['ST'].sum()
    other_S1_sum = below_cutoff['S1'].sum()
    other_interactions_sum = below_cutoff['interactions'].sum()
    bars = bars[bars['ST'] >= other_cutoff]
    if other_ST_sum > 0:
        other_row = pd.DataFrame({
            'inputs': ['Other'],
            'ST': [other_ST_sum],
            'S1': [other_S1_sum],
            'interactions': [other_interactions_sum]
        })
        bars = pd.concat([bars, other_row], ignore_index=True)
    bars = bars.sort_values(by='ST', ascending=False).reset_index(drop=True)
    return bars

def plot_sobol_data(bars, output_formatted, ax, input_to_combined, seen_labels):
    """
    Plots Sobol sensitivity analysis data as horizontal bar charts.

    This function takes processed Sobol data and visualizes it as horizontal bar charts 
    to show the percentage of output variance attributed to each input variable.

    Parameters
    ----------
    bars : pandas.DataFrame
        DataFrame containing the percentage contributions of the total-order (ST), 
        first-order (S1), and interaction effects for each input variable.
    output_formatted : str
        The formatted name of the output variable for labeling the plot.
    ax : matplotlib.axes.Axes
        The axes object on which to plot the data.
    input_to_combined : dict
        A dictionary mapping input variable names to their corresponding combined 
        formatted names and colors. The keys are input variable names, and the values 
        are dictionaries with 'formatted_name' and 'color' keys.
    seen_labels : set
        A set of already seen labels to avoid duplicate labels in the legend.

    Notes
    -----
    1. If the bars DataFrame is empty, a transparent bar is plotted as a placeholder.
    2. Aggregates bars left positions to stack multiple bars horizontally.
    3. Assigns a hatch pattern for the 'Other' category for visual distinction.
    4. Updates the seen_labels set with labels that have already been added to the plot.
    """

    if bars.empty:
        ax.barh(output_formatted, 1, color='none', edgecolor='none')
        return
    
    left_positions = np.zeros(len(bars))
    for i, row in bars.iterrows():
        combined_info = input_to_combined.get(row['inputs'], {'formatted_name': row['inputs'], 'color': 'red'})
        input_name = combined_info['formatted_name']
        color = combined_info['color']
        hatch = '/////' if row['inputs'] == 'Other' else ''
        label = input_name if row['inputs'] not in seen_labels else ""
        seen_labels.add(row['inputs'])
        ax.barh(output_formatted, row['ST'], left=left_positions[i],
                color=color, edgecolor='black', height=0.6,
                label=label, hatch=hatch)
        left_positions = left_positions + row['ST']

    ax.set_xlabel('Percentage of Output Variance', fontsize=18)
    ax.tick_params(labelsize=22)
    ax.set_xticks(np.arange(0, 101, 10))


def plot_sums_of_S1_S2(ax_sum, output_names, S1_sum_list, S2_sum_list):
    """
    Plots the sums of S1 and S2 Sobol indices as horizontal bar charts.

    This function visualizes the cumulative direct and interaction effects of 
    input variables on multiple output variables by plotting the sums of 
    their S1 and S2 Sobol indices.

    Parameters
    ----------
    ax_sum : matplotlib.axes.Axes
        The axes object on which to plot the data.
    output_names : list of str
        List of formatted names of the output variables.
    S1_sum_list : list of floats
        List of sums of the first-order Sobol indices for each output variable.
    S2_sum_list : list of floats
        List of sums of the second-order (interaction) Sobol indices for each output variable.

    Notes
    -----
    1. Ensures the lengths of output_names, S1_sum_list, and S2_sum_list are equal before plotting.
    2. Plots S1 values as gray bars and S2 values as light gray bars stacked on top of S1.
    3. Hides the top and right spines for a cleaner plot appearance.
    4. Layout is adjusted for tight fit within the figure window.
    """

    if len(output_names) == len(S1_sum_list) == len(S2_sum_list):
        ax_sum.barh(output_names, S1_sum_list, color='gray', edgecolor='black', height=0.6, label='Direct Effects')
        ax_sum.barh(output_names, S2_sum_list, color='lightgray', edgecolor='black', height=0.6, label='Interactions', left=S1_sum_list)
    else:
        print("Mismatch in lengths of lists, skipping plot.")

    ax_sum.set_xlabel('Percentage of Output Variance', fontsize=18)
    ax_sum.tick_params(labelsize=22)
    # ax_sum.legend(loc='upper right', bbox_to_anchor=(1.3, 1.01), fontsize=14)
    ax_sum.set_xticks(np.arange(0, 101, 25))
    ax_sum.spines['top'].set_visible(False)
    ax_sum.spines['right'].set_visible(False)
    plt.tight_layout()


# Initialize naming functions
gen_path, indiv_path, structure_path, AMI_BLUE_PATH, BOS_BLUE_PATH, CAV_BLUE_PATH = naming_function.path_names()
df_AMI_sims_label, df_BOS_sims_label, df_CAV_sims_label = naming_function.df_labels()
models = naming_function.model_names()
models.append(['EC', 'Energy Cascade'])

# Master dictionary for storing all input's combined information
master_input_combined = {}

for model in models:
    model_short_name = model[0]
    GSUA_type = f'{model_short_name}_expanded'
    if model_short_name == 'EC':
        GSUA_type = "Energy_Cascade"
    inputs = naming_function.mec_input_names(GSUA_type)
    outputs = naming_function.mec_output_names()

    sobol_cutoff = 0.001
    other_cutoff = 2.5
    S1_df = pd.read_csv(f'{indiv_path}/GSUA_{model_short_name}_out/data/{model_short_name}_sobol_S1_out.csv')
    ST_df = pd.read_csv(f'{indiv_path}/GSUA_{model_short_name}_out/data/{model_short_name}_sobol_ST_out.csv')

    # Create a mapping from input names to combined formatted names and colors
    input_to_combined = {input[0]: {'formatted_name': input[3], 'color': input[4]} for input in inputs}

    # Hard code the color for 'TEMP' and 'OTHER'
    input_to_combined['TEMP'] = {'formatted_name': 'TEMP', 'color': '#004c6d'}
    input_to_combined['Other'] = {'formatted_name': 'Other', 'color': 'lightgray'}

    if 'T_LIGHT' in input_to_combined:
        del input_to_combined['T_LIGHT']
    
    if "T_DARK" in input_to_combined:
        del input_to_combined['T_DARK']

    # Update the master dictionary with the current input_to_combined mapping, avoiding duplicates
    master_input_combined.update(input_to_combined)

    variables = S1_df['Index']

    fig, ax = plt.subplots(figsize=(14, 10))
    fig_sum, ax_sum = plt.subplots(figsize=(7, 10))

    total_st_values = {output[0]: ST_df[f'{output[0]}_ST'].sum() if f'{output[0]}_ST' in ST_df.columns else 0 for output in outputs}
    sorted_outputs = sorted(outputs, key=lambda x: total_st_values[x[0]], reverse=False)

    S1_sum_list = []
    S2_sum_list = []
    output_names = []

    seen_labels = set()

    for output in sorted_outputs:
        if output[0] == 'g_A':
            continue
        
        output_names.append(output[3])
        bars = process_and_prepare_bars(S1_df, ST_df, output[0], variables, sobol_cutoff)
        plot_sobol_data(bars, output[3], ax, input_to_combined, seen_labels)

        # Summarize the direct and interaction effects
        S1_sum_list.append(bars['S1'].sum())
        S2_sum_list.append(bars['interactions'].sum())
        print(model_short_name, output[0], S2_sum_list[-1])

    plot_sums_of_S1_S2(ax_sum, output_names, S1_sum_list, S2_sum_list)
    
    handles, labels = ax.get_legend_handles_labels()
    
    by_label = dict(zip(labels, handles))
    # ax.legend(by_label.values(), by_label.keys(), loc='upper right', bbox_to_anchor=(1.2, 1.01), fontsize=14)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    timer = fig.canvas.new_timer(interval=8000)
    timer.add_callback(plt.close)
    timer.start()
    
    fig.savefig(f'{gen_path}/{model_short_name}_SOBOL_ST.png', bbox_inches='tight')
    fig_sum.savefig(f'{gen_path}/{model_short_name}_SOBOL_S1_S2.png', bbox_inches='tight')
    plt.show()

# Creating an all-encompassing Legend
sorted_colors = [
    '#004c6d', '#377290', '#609ab4', '#8ac4d9', '#b6efff', # glacier
    '#88011b', '#a94542', '#c8756e', '#e5a59d', '#ffd6d0', # crimson
    '#4a6fe3', '#788beb', '#9ea8f2', '#c0c5f9', '#e2e4ff', # periwinkle
    '#d33f6a', '#e16989', '#ed8ea7', '#f7b2c4', '#ffd5e1', # pink
    '#0d952a', '#50ac51', '#7bc477', '#a3db9e', '#caf3c5', # green
    '#cd8207', '#db9a3e', '#e7b266', '#f4c98e', '#ffe1b6', # gold
    '#0a867c', '#3ea197', '#61bdb2', '#82dacf', '#a3f7ec', # teal
    '#a2668b', '#b981a6', '#d09dc2', '#e7bade', '#ffd7fa', # violet
    '#696939', '#888753', '#a8a76d', '#c9c789', '#ebe9a6'  # military green
]

sorted_master_dict = {}

for color in sorted_colors:
    for key, value in master_input_combined.items():
        if value['color'] == color:
            sorted_master_dict[key] = value

sorted_master_dict['Other'] = {'formatted_name': 'Other', 'color': 'lightgray'}
sorted_master_dict['S1'] = {'formatted_name': 'Sum of S1', 'color': 'gray'}
sorted_master_dict['S2'] = {'formatted_name': 'Sum of S2', 'color': 'lightgray'}

# Create the master legend figure
fig, ax = plt.subplots(figsize=(6, len(sorted_master_dict) * 0.3))

# Create patches for the master legend using combined information
patches = []
for key, info in sorted_master_dict.items():
    if key == 'Other':
        patches.append(mpatches.Patch(facecolor=info['color'], label=info['formatted_name'], hatch='////', edgecolor='black'))
    else:
        patches.append(mpatches.Patch(facecolor=info['color'], label=info['formatted_name'], edgecolor='black'))

# Add the legend to the figure
ax.legend(handles=patches, loc='center', ncol=1, fontsize=18, frameon=False)
ax.axis('off')  # Hide the axes

plt.tight_layout()
plt.savefig(f'[INSERT YOUR PATH HERE]', bbox_inches='tight')
plt.show()