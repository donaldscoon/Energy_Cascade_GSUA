"""
Amitrano et. al. Modified Energy Cascade Crop Systems Model

Author: Donald Coon
Date: January 2025
Description: 
    Calculates the Total Edible Biomass (TEB) and Transpiration Rate (DTR) in response to daily environmental data.

    This script is designed to be run from the command line, as part of a high-performance computing workflow.
    It is tailored for  simulation studies, such as Global Sensitivity and Uncertainty Analysis (GSUA),
    and records data at each timestep to facilitate post-simulation analysis.

Citation:
    This script recreates the work detailed in the peer-reviewed publication 
    Amitrano, C.; Chirico, G.B.; De Pascale, S.; Rouphael, Y.; De Micco, V. 
    Crop Management in Controlled Environment Agriculture (CEA) Systems Using Predictive Mathematical Models. 
    Sensors 2020, 20, 3110, doi:10.3390/s20113110.

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

import sys
import numpy as np
import pandas as pd
import naming_function

pd.set_option('display.max_columns', None)          # Show all the columns in the dataframe when printed
pd.set_option('display.max_colwidth', None)         # Show the full content of the cells without truncation
pd.set_option('display.expand_frame_repr', False)   # Display columns side by side rather than wrapping them

# Retrieve all necessary paths from the naming function
gen_path, _, _, AMI_BLUE_PATH, _, _ = naming_function.path_names()

def RUN_SIM(SIM_NUM, SIM_TEMP, SIM_RH, SIM_CO2, SIM_PPFD, SIM_H, 
            SIM_P_ATM, SIM_BCF, SIM_XFRT, SIM_OPF, 
            SIM_g_A, SIM_t_E, SIM_t_Mi, SIM_amin_GN, SIM_amax_GN, SIM_bmin_GN, 
            SIM_bmax_GN, SIM_amin_GON, SIM_amax_GON, SIM_bmin_GON, 
            SIM_bmax_GON):
    """
    Run the simulation with the specified parameters.

    Parameters:
    SIM_NUM (int): Simulation number.
    SIM_TEMP (float): Temperature during the light cycle (°C).
    SIM_RH (float): Relative Humidity (fraction between 0 and 1).
    SIM_CO2 (float): CO2 concentration (µmol CO2 / mol air).
    SIM_PPFD (float): Photosynthetic Photon Flux Density (µmol/m²/s).
    SIM_H (int): Number of hours of the photoperiod.
    SIM_P_ATM (float): Atmospheric pressure (kPa).
    SIM_BCF (float): Biomass Carbon Fraction (fraction).
    SIM_XFRT (float): Edible Biomass Fraction (fraction).
    SIM_OPF (float): Oxygen Production Fraction (fraction).
    SIM_g_A (float): atmospheric conductance factor.
    SIM_t_E (float): time until edible organ formation starts.
    SIM_t_Mi (float): Maturation time of initial biomass.
    SIM_amin_GN, SIM_amax_GN, SIM_bmin_GN, SIM_bmax_GN (float): Crop specific parameteres for green lettuce under nominal VPDs
    SIM_amin_GON, SIM_amax_GON, SIM_bmin_GON, SIM_bmax_GON (float): Crop specific parameteres for green lettuce under off-nominal VPDs

    Returns:
    None. Prints simulation results as a DataFrame to the console.
    """

    df_sims = pd.DataFrame({})
    path = AMI_BLUE_PATH

    PPFD = SIM_PPFD       # umol/m^2/sec
    CO2 = SIM_CO2         # umol CO2 / mol air
    H = SIM_H             # photoperiod
    T_LIGHT = SIM_TEMP    # Light Cycle Average Temperature
    T_DARK = T_LIGHT -  5 # Dark Cycle Average. 
    RH = SIM_RH           # Relative Humidty as a fraction bounded between 0 and 1.
    t_M = 35              # time at harvest/maturity ewert table 4-112
    P_ATM = SIM_P_ATM     # atmospheric pressure
    T_T = 10              # days to transplant, based on experimental design of Amitrano 2020


    ##################################################
    ################# INTIALIZATION  #################
    ##################################################

    t = 0                           # time in days
    res = 1                         # model resolution (in days)
    day = 0                         # counter used in handling the seedling stage loop
    df_records = pd.DataFrame({})   # simulation record dataframe
    ts_to_harvest = int(t_M/res)    # calculates the timesteps needed to set up the matrix for each ts
    TEB = 8.53                      # The value of TEB at 10 DAE

    ##################################################
    #################### CONSTANTS ###################
    ##################################################
    BCF = SIM_BCF       # Biomass Carbon Fraction
    XFRT = SIM_XFRT     # Edible Biomass Fraction
    OPF = SIM_OPF       # Oxygen Production Fraction
    g_A = SIM_g_A       # Atmospheric Conductance
    t_D = 1             # 1 for green, 8 for red initial time of development(days) Amirtrano 2020 CQY experiments
    t_Mi = SIM_t_Mi     # initial time of maturity (days)
    t_E = SIM_t_E       # time at onset of organ formation 
    MWC = 12.01         # molecular weight of carbon 
    MW_W = 18.015       # molecular weight of water 
    d_W = 998.23        # water density 

    # This first loop is needed to align dataframe across models.
    # It is the first 10 days from seedling to transplant. 
    while t < T_T:
        dfts = pd.DataFrame({
            'SIM_NUM': [SIM_NUM],
            'Timestep': [t]}) # ,
            # 'Day': [day]})
        df_records = pd.concat([df_records, dfts], ignore_index=True) 
        t += res

    # This second loop continues from transplant to harvest.
    # while time is less than harvest time
    while t <= ts_to_harvest:
        VP_SAT = 0.611*np.exp(1)**(17.4*T_LIGHT/(T_LIGHT+239)) # Vapor Pressure of Saturation (kPa)
        VP_AIR = VP_SAT*RH          # Vapor Pressure of Air (kPa)
        VPD = VP_SAT*(1-RH)         # Vaport Pressure Defecit (kPa)
        if VPD <= 1.225:            # Assuming the nominal inflection point as it is halfway between 0.69(NOM) and 1.76(OFFNOM)
            amin = SIM_amin_GN
            amax = SIM_amax_GN
            bmin = SIM_bmin_GN
            bmax = SIM_bmax_GN
        else:
            amin = SIM_amin_GON
            amax = SIM_amax_GON
            bmin = SIM_bmin_GON
            bmax = SIM_bmax_GON
        if t<= t_D:         # if timestep is before formation of edible organs
            ALPHA = amin    # amitrano 2020 eq 15
            BETA = bmin     # amitrano 2020 eq 15
        elif t <= t_Mi:     # if timestep is after organ formation but before maturity
            ALPHA = amin+(amax-amin)*(t-t_D)/(t_Mi-t_D)        # amitrano 2020 eq 15
            BETA = bmin+(bmax-bmin)*(t-t_D)/(t_Mi-t_D)         # amitrano 2020 eq 15
        else:                # all other timesteps
            ALPHA = amax     # amitrano 2020 eq 15
            BETA = bmax      # amitrano 2020 eq 15
        DCG = 0.0036*H*ALPHA*PPFD              # Daily Carbon Gain (mol_carbon m^-2 day^-1)
        DOP = OPF*DCG                          # Daily Oxygen Production (mol_oxygen m^-2 day^-1)
        CGR = MWC*(DCG/BCF)                    # Crop Growth Rate (grams m^-2 day^-1)
        # if edible organ formation has begun
        if t > t_E:                 
            TEB = CGR+TEB                                       # Total Edible Biomass (grams m^-2 day^-1)
        P_GROSS = BETA*PPFD                                     # Gross Photosynthesis (umol_carbon m^-2 second^-1)
        P_NET = (H*ALPHA/24+BETA*(24-H)/24)*PPFD                # Net Photosynthesis(umol_carbon m^-2 second^-1)
        g_S = ((1.717*T_LIGHT)-19.96-(10.54*VPD))*(P_NET/CO2)   # Stomatal Conductance (mol_water m^-2 second^-1)
        g_C = g_A*g_S/(g_A+g_S)                                 # Canopy Conductance (mol_water m^-2 second^-1)
        DTR = 3600*H*(MW_W/d_W)*g_C*(VPD/P_ATM)                 # Daily Transpiration Rate (L_water m^-2 day^-1)

        # Creates a dataframe of all variables/outputs for each timestep.
        dfts = pd.DataFrame({
            'SIM_NUM': [SIM_NUM],
            'Timestep': [t],
            'H': [H],
            'A': [0],        # Not included but retained for processing ease
            'ALPHA':[ALPHA],
            'BETA':[BETA],
            'CQY': [0],      # Not included but retained for processing ease
            'CUE_24': [0],   # Not included but retained for processing ease
            'DCG': [DCG],
            'CGR': [CGR],
            'TCB': [0],      # Not included but retained for processing ease
            'TEB': [TEB],
            'DOP': [DOP],
            'VP_SAT': [VP_SAT],
            'VP_AIR': [VP_AIR],
            'VPD': [VPD],
            'P_GROSS': [P_GROSS],
            'P_NET': [P_NET],
            'g_S': [g_S],
            'g_A': [g_A],
            'g_C': [g_C],
            'DTR': [DTR],
            'T_LIGHT': [T_LIGHT],
            'T_DARK': [T_DARK],
            'RH': [RH],
            'CO2': [CO2],
            'PPFD': [PPFD],
            'P_ATM': [SIM_P_ATM],
            'BCF': [SIM_BCF],
            'XFRT': [SIM_XFRT],
            'OPF': [SIM_OPF],
            'g_A': [SIM_g_A],
            't_Mi': [SIM_t_Mi],
            't_E': [SIM_t_E],
            'amin_GN': [SIM_amin_GN], 
            'amax_GN': [SIM_amax_GN], 
            'bmin_GN': [SIM_bmin_GN], 
            'bmax_GN': [SIM_bmax_GN], 
            'amin_GON': [SIM_amin_GON],
            'amax_GON': [SIM_amax_GON], 
            'bmin_GON': [SIM_bmin_GON], 
            'bmax_GON': [SIM_bmax_GON], 
        })  
        df_records = pd.concat([df_records, dfts], ignore_index=True) # this adds the timestep dataframe to the historical values dataframe
        # advance timestep
        t += res
    # prints to console, which is captured as an HPC output
    print(df_records.to_string(index=False, header=False))                    # prints a copy of output in the terminal

# Executes this program/function
if __name__ == "__main__":
    # Parse command-line arguments
    args = sys.argv[1:]
    if len(args) != 21:
        print(f"Expected 21 arguments, but got {len(args)}")
        sys.exit(1)

    # Convert arguments to appropriate types
    SIM_NUM = int(args[0])
    params = list(map(float, args[1:]))

    # Call RUN_SIM with the parsed arguments
    RUN_SIM(SIM_NUM, *params)
