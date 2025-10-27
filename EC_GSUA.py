"""
Volk et. al. Modified Energy Cascade Crop Systems Model

Author: Donald Coon
Date: January 2025
Description: 
    Calculates the Total Edible Biomass (TEB) in response to daily environmental data.

    This script is designed to be run from the command line, as part of a high-performance computing workflow.
    It is tailored for  simulation studies, such as Global Sensitivity and Uncertainty Analysis (GSUA),
    and records data at each timestep to facilitate post-simulation analysis.

Citation:
    This script recreates the work detailed in the peer-reviewed publication 
    Volk, T.; Bugbee, B.; Wheeler, R.M. 
    An Approach to Crop Modeling with the Energy Cascade. 
    Life Support Biosph Sci 1995, 1, 119–127.
    
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

gen_path, EC_BLUE_PATH, GSUA_type = naming_function.EC_info()


def RUN_SIM(SIM_NUM, SIM_PPFD, SIM_H, SIM_K, SIM_C, 
            SIM_t_a, SIM_t_m, SIM_A_MAX, SIM_Q_min, SIM_Q_max
            ): # used to package this version of the MEC as a function callable by other programs

    """
    Run the simulation with the specified parameters.

    Parameters:
    SIM_NUM (int): Simulation number.
    SIM_PPFD (float): Photosynthetic Photon Flux Density (µmol/m²/s).
    SIM_H (int): Number of hours of the photoperiod.
    SIM_K (float): Conversion constant
    SIM_C (float): Carbon Use Efficency
    SIM_t_a (float): Time of canopy closure (days)
    SIM_t_m (float): Time of crop maturity (days)
    SIM_A_MAX (float): Fraction of PPFD absorbed after t=t_a 
    SIM_Q_min (float): canopy quantum yield at t=t_m
    SIM_Q_max (float): canopy quantum yield until t=t_Q 
    """
    t = 0                       # Initialization of time (days)
    B = 0                       # starting crop biomass
    df_records = pd.DataFrame({}) 

    PPFD = SIM_PPFD             # umol/m^2/sec
    H = SIM_H                   # photoperiod (hours)
    T = 20                      # daily average temperature (C), unused, but present in Volk Table 2

    K = SIM_K                   # Conversion constant 
    C = SIM_C                   # Carbon Use Efficency

    t_a = SIM_t_a               # Time of canopy closure (days)
    t_m = SIM_t_m               # Time of crop maturity (days)
    t_Q = 50                    # Time of onset of canopy senescence (days)
    t_f = 35                    # Length of simulation in timesteps (days) AKA: Harvest
    t_s = 1                     # Timestep (day)

    A_max = SIM_A_MAX           # Fraction of PPFD absorbed after t=t_a
    Q_min = SIM_Q_min           # canopy quantum yield at t=t_m 
    Q_max = SIM_Q_max           # canopy quantum yield until t=t_Q

    # while time is less than harvest
    while t <= t_f:
        # Before canopy closure
        if t <= t_a: 
            A = (A_max/t_a)*t   # Photon Absorption
        
        # After canopy closure
        elif t > t_a: 
            A = A_max           # Photon Absorption
        
        # before onset of senescence
        if t <= t_Q:
            Q = Q_max           # Canopy Quantum Yield umol_fixed /umol_aborbed
        elif t > t_Q:
            Q = Q_max - ((Q_max-Q_min)/(t_m-t_Q))*(t-t_Q)   # Canopy Quantum Yield umol_fixed /umol_aborbed

        P_GROSS = Q*A*PPFD # Gross Photosynthesis (umol_carbon m^-2 second^-1)
        P_NET = C*Q*A*PPFD # Net Photosynthesis(umol_carbon m^-2 second^-1)
        R = (1-C)*Q*A*PPFD # Respiration (umol_carbon m^-2 second^-1)
        CGR = K*(H*P_NET-(24-H)*R) # Crop Growth Rate (grams m^-2 day^-1)
        B += CGR # Total Crop Biomass (grams m^-2 day^-1)

        # Creates a dataframe of all variables/outputs for each timestep.
        dfts = pd.DataFrame({
            'SIM_NUM': [SIM_NUM],
            'timestep': [t],
            'A': [A],
            'A_MAX': [A_max],
            'CQY': [Q],
            'CQY_MIN': [Q_min],
            'CQY_MAX': [Q_max],
            'CUE_24': [C],
            'P_GROSS': [P_GROSS],
            'P_NET': [P_NET],
            'RESP': [R],
            'CGR': [CGR],
            'TCB': [B],
            'H': [H],
            'PPFD': [PPFD],
            'T_LIGHT': [T],
        })
        df_records = pd.concat([df_records, dfts], ignore_index=True) # this adds the timestep dataframe to the historical values dataframe
        # advance timestep
        t += t_s 
    # prints to console, which is captured as an HPC output          
    print(df_records.to_string(index=False, header=False))


# Executes this program/function
if __name__ == "__main__":
    # Parse command-line arguments
    args = sys.argv[1:]
    if len(args) != 10:
        print(f"Expected 10 arguments, but got {len(args)}")
        sys.exit(1)

    # Convert arguments to appropriate types
    SIM_NUM = int(args[0])
    params = list(map(float, args[1:]))

    # Call RUN_SIM with the parsed arguments
    RUN_SIM(SIM_NUM, *params)
