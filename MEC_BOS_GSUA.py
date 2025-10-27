"""
Boscheri et. al. Modified Energy Cascade Crop Systems Model

Author: Donald Coon
Date: January 2025
Description: 
    Calculates the Total Edible Biomass (TEB) and Transpiration Rate (HTR) in response to hourly environmental data.

    This script is designed to be run from the command line, as part of a high-performance computing workflow.
    It is tailored for  simulation studies, such as Global Sensitivity and Uncertainty Analysis (GSUA),
    and records data at each timestep to facilitate post-simulation analysis.

Citation:
    This script recreates the work detailed in the peer-reviewed publication 
    Boscheri, G.; Kacira, M.; Patterson, L.; Giacomelli, G.; Sadler, P.; Furfaro, R.; Lobascio, C.; Lamantea, M.; Grizzaffi, L. 
    Modified Energy Cascade Model Adapted for a Multicrop Lunar Greenhouse Prototype. 
    Advances in Space Research 2012, 50, 941–951, doi:10.1016/j.asr.2012.05.025.

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
gen_path, _, _, _, BOS_BLUE_PATH, _ = naming_function.path_names()

def RUN_SIM(SIM_NUM, SIM_TEMP, SIM_RH, SIM_CO2, SIM_PPFD, SIM_H,
            SIM_P_ATM, SIM_BCF, SIM_XFRT, SIM_OPF, SIM_g_A, SIM_A_MAX, SIM_t_E, SIM_CQY_MIN, SIM_CUE_MAX, SIM_CUE_MIN,
            SIM_D_PG, SIM_n , SIM_DRY_FR, SIM_NC_FR, SIM_ta_c2, SIM_ta_c3, SIM_ta_c5, SIM_ta_c7, SIM_ta_c9, 
            SIM_ta_c11, SIM_cqy_max_c7 , SIM_cqy_max_c8 , SIM_cqy_max_c9 , SIM_cqy_max_c12, SIM_cqy_max_c18, 
            SIM_cqy_max_c19):
    
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
    SIM_g_A (float): Atmospheric conductance factor.
    SIM_A_MAX (float): Maximum canopy photon absorption .
    SIM_t_E (float):  Time of Organ Formation (days).
    SIM_CQY_MIN (float): Minimum Canopy Quantum Yield (umol CO2 fixed/umol photons absorbed).
    SIM_CUE_MAX (float): Maximum Carbon Use Efficiency (fraction).
    SIM_CUE_MIN (float): Minimum Carbon Use Efficiency (fraction).
    SIM_D_PG (float): Duration of the day (hours).
    SIM_n (float): Crop Specific Exponent
    SIM_DRY_FR (float): Dry matter fraction of the biomass (fraction).
    SIM_NC_FR (float): Nutrient consumption rate of the biomass (fraction).
    SIM_ta_c2, SIM_ta_c3, SIM_ta_c5, SIM_ta_c7, SIM_ta_c9, , SIM_ta_c11 (float): Canopy Closure coefficients
    SIM_cqy_max_c7, SIM_cqy_max_c8, SIM_cqy_max_c9, SIM_cqy_max_c12, SIM_cqy_max_c18, SIM_cqy_max_c19 (float): Maximum Canopy Quantum Yield coefficient

    Returns:
    None. Prints simulation results as a DataFrame to the console.
    """

    df_sims = pd.DataFrame({})
    path = BOS_BLUE_PATH
    
    PPFD = SIM_PPFD             # umol/m^2/sec
    CO2 = SIM_CO2               # umol CO2 / mol air
    H = round(SIM_H, 0)         # photoperiod, rounded to a whole number
    T_LIGHT = SIM_TEMP          # Light Cycle Average Temperature ewert table 4-111 or user input
    T_DARK = T_LIGHT - 5        # Dark Cycle Average Temperature ewert table 4-111 or user input
    RH = SIM_RH                 # Relative Humidty as a fraction bounded between 0 and 1.
    t_M = 35                    # time at harvest/maturity ewert table 4-112
    P_ATM = SIM_P_ATM           # atmospheric pressure
    D_PG = round(SIM_D_PG, 0)   # the plants diurnal cycle length, rounded

    ##################################################
    ################# INTIALIZATION  #################
    ##################################################
    t = 0                           # time in days
    res = 1                         # model resolution (hours)
    I = 0                           # "I is equal to 1 and 0 during the photoperiod (day) and dark period (night)"
    night_len = D_PG - round(H, 0)  # length of night (rounded so the decimals don't break day/night cycle)
    day_len = D_PG - night_len      # length of day (hours)
    pp_count = 0                    # photoperiod counter
    day = 0

    ##################################################
    ############    ######## CONSTANTS ###################
    ##################################################
    BCF = SIM_BCF           # Biomass Carbon Fraction
    XFRT = SIM_XFRT         # Edible Biomass Fraction
    OPF = SIM_OPF           # Oxygen Production Fraction
    g_A = SIM_g_A           # Atmospheric Conductance 
    A_max = SIM_A_MAX       # maximum fraction of PPF Absorbtion 
    t_Q = 50                # onset of senescence placeholder value ewert table 4-112
    t_E = SIM_t_E           # time at onset of organ formation (days)
    MW_W = 18.0153          # Molecular weight of water
    MWC = 12.0107           # molecular weight of carbon
    MW_O2 = 31.9988         # molecular weight of O2
    MW_CO2 = 44.010         # molecular weight of CO2
    CQY_min = SIM_CQY_MIN   # minimum canopy quantum
    CUE_max = SIM_CUE_MAX   # maximum carbon use efficiency
    CUE_min = SIM_CUE_MIN   # minimum carbon use efficiency 
    p_W = 998.23            # density of water at 20 C
    n = SIM_n               # crop specific exponent
    a = 0.0036              # conversion factor boscheri table 4 
    b = 3600                # conversion factor boscheri table 4
    WBF = XFRT              # Boscheri doesn't define this, I'm assuming that its the same as XFRT
    DRY_FR = SIM_DRY_FR     # dry over wet biomass fraction 
    NC_FR = SIM_NC_FR       # Nutrient Consumption Rate of Fresh Mass

    df_records = pd.DataFrame({})
    ts_to_harvest = int(t_M*24/res)     # calcs the timesteps needed to set up the matrix for each ts
    TCB = 0                             # starting crop biomass
    TEB = 0                             # starting total edible biomass

    ##################################################
    ############# SUPPLEMENTAL EQUATIONS #############
    ##################################################
    """ Multipolynomial Regression Coefficients Ewert Table 4-100 """
    # used in the calculation of A_max and CQY_max

    c1 = (1/PPFD)*(1/CO2)
    c2 = (1/PPFD)
    c3 = (CO2/PPFD)
    c4 = (CO2**2/PPFD)
    c5 = (CO2**3/PPFD)
    c6 = (1/CO2)
    c7 = 1
    c8 = CO2
    c9 = (CO2**2)
    c10 = (CO2**3)
    c11 = PPFD*(1/CO2)
    c12 = PPFD
    c13 = PPFD*CO2
    c14 = PPFD*(CO2**2)
    c15 = PPFD*(CO2**3)
    c16 = (PPFD**2)*(1/CO2)
    c17 = (PPFD**2)
    c18 = (PPFD**2)*CO2
    c19 = (PPFD**2)*(CO2**2)
    c20 = (PPFD**2)*(CO2**3)
    c21 = (PPFD**3)*(1/CO2)
    c22 = (PPFD**3)
    c23 = (PPFD**3)*CO2
    c24 = (PPFD**3)*(CO2**2)
    c25 = (PPFD**3)*(CO2**3)


    """ Canopy Closure t_A """
    # Only 2,3,5,7,9,11 are used for lettuce Ewert table 4-115 
    tac1 = 0
    tac2 = SIM_ta_c2
    tac3 = SIM_ta_c3
    tac4  = 0 
    tac5 = SIM_ta_c5
    tac6 = 0
    tac7 = SIM_ta_c7
    tac8 = 0
    tac9 = SIM_ta_c9
    tac10 = 0
    tac11 = SIM_ta_c11
    tac12 = 0
    tac13 = 0
    tac14 = 0
    tac15 = 0
    tac16 = 0
    tac17 = 0
    tac18 = 0
    tac19 = 0
    tac20 = 0
    tac21 = 0
    tac22 = 0
    tac23 = 0
    tac24 = 0
    tac25 = 0

    # each term in the t_A Ewert eq 4-30
    t_A_1 = tac1*c1
    t_A_2 = tac2*c2
    t_A_3 = tac3*c3
    t_A_4 = tac4*c4
    t_A_5 = tac5*c5
    t_A_6 = tac6*c6
    t_A_7 = tac7*c7
    t_A_8 = tac8*c8
    t_A_9 = tac9*c9
    t_A_10 = tac10*c10
    t_A_11 = tac11*c11
    t_A_12 = tac12*c12
    t_A_13 = tac13*c13
    t_A_14 = tac14*c14
    t_A_15 = tac15*c15
    t_A_16 = tac16*c16
    t_A_17 = tac17*c17
    t_A_18 = tac18*c18
    t_A_19 = tac19*c19
    t_A_20 = tac20*c20
    t_A_21 = tac21*c21
    t_A_22 = tac22*c22
    t_A_23 = tac23*c23
    t_A_24 = tac24*c24
    t_A_25 = tac25*c25

    # the calculation of canopy closure ewert eq 4-30
    t_A = (t_A_1 + t_A_2 + t_A_3 + t_A_4 + t_A_5 + 
        t_A_6 + t_A_7 + t_A_8 + t_A_9 + t_A_10 + 
        t_A_11 + t_A_12 + t_A_13 + t_A_14 + t_A_15 + 
        t_A_16 + t_A_17 + t_A_18 + t_A_19 + t_A_20 + 
        t_A_21 + t_A_22 + t_A_23 + t_A_24 + t_A_25)

    """ Canopy Quantum Yield Equation """
    # only 7,8,9,12,18,19 are used for lettuce ewert table 4-102
    CQY_m_c_1 = 0
    CQY_m_c_2 = 0
    CQY_m_c_3 = 0
    CQY_m_c_4 = 0
    CQY_m_c_5 = 0
    CQY_m_c_6 = 0
    CQY_m_c_7 = SIM_cqy_max_c7
    CQY_m_c_8 = SIM_cqy_max_c8
    CQY_m_c_9 = SIM_cqy_max_c9
    CQY_m_c_10 = 0
    CQY_m_c_11 = 0
    CQY_m_c_12 = SIM_cqy_max_c12
    CQY_m_c_13 = 0
    CQY_m_c_14 = 0
    CQY_m_c_15 = 0
    CQY_m_c_16 = 0
    CQY_m_c_17 = 0
    CQY_m_c_18 = SIM_cqy_max_c18
    CQY_m_c_19 = SIM_cqy_max_c19
    CQY_m_c_20 = 0
    CQY_m_c_21 = 0
    CQY_m_c_22 = 0
    CQY_m_c_23 = 0
    CQY_m_c_24 = 0
    CQY_m_c_25 = 0

    # CQY_max Terms ewert eq 4-22
    CQY_m_t_1 = CQY_m_c_1*c1
    CQY_m_t_2 = CQY_m_c_2*c2
    CQY_m_t_3 = CQY_m_c_3*c3
    CQY_m_t_4 = CQY_m_c_4*c4
    CQY_m_t_5 = CQY_m_c_5*c5
    CQY_m_t_6 = CQY_m_c_6*c6
    CQY_m_t_7 = CQY_m_c_7*c7
    CQY_m_t_8 = CQY_m_c_8*c8
    CQY_m_t_9 = CQY_m_c_9*c9
    CQY_m_t_10 = CQY_m_c_10*c10
    CQY_m_t_11 = CQY_m_c_11*c11
    CQY_m_t_12 = CQY_m_c_12*c12
    CQY_m_t_13 = CQY_m_c_13*c13
    CQY_m_t_14 = CQY_m_c_14*c14
    CQY_m_t_15 = CQY_m_c_15*c15
    CQY_m_t_16 = CQY_m_c_16*c16
    CQY_m_t_17 = CQY_m_c_17*c17
    CQY_m_t_18 = CQY_m_c_18*c18
    CQY_m_t_19 = CQY_m_c_19*c19
    CQY_m_t_20 = CQY_m_c_20*c20
    CQY_m_t_21 = CQY_m_c_21*c21
    CQY_m_t_22 = CQY_m_c_22*c22
    CQY_m_t_23 = CQY_m_c_23*c23
    CQY_m_t_24 = CQY_m_c_24*c24
    CQY_m_t_25 = CQY_m_c_25*c25

    # CQY_max Calculation ewert eq 4-22
    CQY_max = (CQY_m_t_1 + CQY_m_t_2 + CQY_m_t_3 + CQY_m_t_4 + CQY_m_t_5 +
            CQY_m_t_6 + CQY_m_t_7 + CQY_m_t_8 + CQY_m_t_9 + CQY_m_t_10 + 
            CQY_m_t_11 + CQY_m_t_12 + CQY_m_t_13 + CQY_m_t_14 + CQY_m_t_15 + 
            CQY_m_t_16 + CQY_m_t_17 + CQY_m_t_18 + CQY_m_t_19 + CQY_m_t_20 + 
            CQY_m_t_21 + CQY_m_t_22 + CQY_m_t_23 + CQY_m_t_24 + CQY_m_t_25)

    ##################################################
    ################# THE MODEL LOOP #################
    ##################################################
    # while time is less than harvest time
    while t < ts_to_harvest:                
        if I == 0 and pp_count == night_len:    # turns night to day
            I = 1
            pp_count = 0
        elif I == 1 and pp_count == day_len:    # turns day to night
            I = 0
            pp_count = 0
        if t > 0 and (t % D_PG) == 0:           # this if statement counts the days by checking if the ts/24 is a whole number
            day += 1
        # before canopy closure
        if t < (t_A*D_PG/res):                  
            A = A_max*(t/(t_A*D_PG/res))**n     # Photon Absorption
        # after canopy closure
        else:                        
            A = A_max                           # Photon Absorption
        # before onset of senescence
        if t<= t_Q:                  
            CQY = CQY_max       # Canopy Quantum Yield umol_fixed umol_aborbed
            CUE_24 = CUE_max    # Carbon Use Efficiency
        elif (t_Q*24/res) < t: 
            """For lettuce the values of CQY_min and CUE_min 
            are n/a due to the assumption that the canopy does
            not senesce before harvest. I coded them anyways, it
            makes it complete for all the other crops too. For 
            crops other than lettuce remove the break statement."""
            CQY = CQY_max - (CQY_max - CQY_min)*((t-t_Q)/(t_M-t_Q)) # boscheri eq 3
            CUE_24 = CUE_max - (CUE_max - CUE_min)*((t-t_Q)/(t_M-t_Q)) # boscheri eq 4
            print(t, "Error: Utilizing CQY and CUE values without definitions")
            break
        HCG = a*CUE_24*A*CQY*PPFD*I             # Hourly Carbon Gain (mol_carbon m^-2 hour^-1)
        HCGR = HCG*MWC*(BCF)**(-1)              # Crop Growth Rate (grams m^-2 hour^-1)
        HWCGR = HCGR*(1-WBF)**(-1)              # Hourly Wet Crop Growth Rate (grams m^-2 hour^-1)
        HOP = HCG/CUE_24*OPF*MW_O2              # Hourly Oxygen Production (mol_oxygen m^-2 Hour^-1)
        HOC = HCG/(1-CUE_24)/CUE_24*OPF*MW_O2*H/24 # Hourly Oxygen Consumption (mol_oxygen m^-2 Hour^-1)
        VP_SAT = 0.611*np.exp(1)**((17.4*T_LIGHT)/(T_LIGHT+239)) # Vapor Pressure of Saturation (kPa)
        VPD = VP_SAT*(1-RH)                     # Vaport Pressure Defecit (kPa)
        P_NET = A*CQY*PPFD                      # Net Photosynthesis(umol_carbon m^-2 second^-1)
        g_S = (1.717*T_LIGHT-19.96-10.54*VPD)*(P_NET/CO2) # Stomatal Conductance (mol_water m^-2 second^-1)
        g_C = (g_A*g_S)*(g_A+g_S)**(-1)         # Canopy Conductance (mol_water m^-2 second^-1)
        # HTR = b*MW_W*g_C*(VPD/P_ATM)          # The original boscheir eq 10 which I believe is missing the density of water
        HTR = b*(MW_W/p_W)*g_C*(VPD/P_ATM)      # Daily Transpiration Rate (L_water m^-2 hour^-1)
        HCO2C = HOP*MW_CO2*MW_O2**(-1)          # Hourly CO2 Consumption
        HCO2P = HOC*MW_CO2*MW_O2**(-1)          # Hourly CO2 Production
        HNC = HCGR*DRY_FR*NC_FR                 # Hourly Nutrient Consumption
        HWC = HTR+HOP+HCO2P+HWCGR-HOC-HCO2C-HNC # Hourly Water Consumption 
        TCB += HCGR                             # Total Crop Biomass (grams m^-2 day^-1)
        # accumilate edible biomass when organ formation begins
        if t > t_E:                      
            TEB += XFRT*HCGR                    # Total Edible Biomass (grams m^-2 day^-1)

        # Creates a dataframe of all variables/outputs for each timestep.
        dfts = pd.DataFrame({
            'SIM_NUM': [SIM_NUM],
            'Timestep': [t],
            'H': [H],
            'Day': [day],
            'diurnal': [I],
            'A': [A],
            'CQY': [CQY],
            'CUE_24': [CUE_24],
            'DCG': [HCG],
            'CGR': [HCGR],
            'DWCGR': [HWCGR],
            'TCB': [TCB],
            'TEB': [TEB],
            'VP_SAT': [VP_SAT],
            'VP_AIR': [0],      # Not included but retained for processing ease
            'VPD': [VPD],
            'P_NET': [P_NET],
            'P_GROSS': [0],     # Not included but retained for processing ease
            'DOP': [HOP],
            'DOC': [HOC],
            'g_S': [g_S],
            'g_A': [g_A],
            'g_C': [g_C],
            'DTR': [HTR],
            'DCO2C': [HCO2C],
            'DCO2P': [HCO2P],
            'DNC': [HNC], 
            'DWC': [HWC],
            'T_LIGHT': [T_LIGHT],
            'T_DARK': [T_DARK],
            'RH': [RH],
            'CO2': [CO2],
            'PPFD': [PPFD],
            'P_ATM': [SIM_P_ATM],
            'BCF': [SIM_BCF],
            'XFRT': [SIM_XFRT],
            'OPF': [SIM_OPF],
            'A_MAX': [SIM_A_MAX],
            't_E': [SIM_t_E],
            'CQY_MIN': [SIM_CQY_MIN],
            'CUE_MIN': [SIM_CUE_MIN],
            'CUE_MAX': [SIM_CUE_MAX],
            'D_PG': [SIM_D_PG],
            'n': [SIM_n],
            'DRY_FR': [SIM_DRY_FR],
            'NC_FR': [SIM_NC_FR],
            'ta_c2': [SIM_ta_c2],
            'ta_c3': [SIM_ta_c3],
            'ta_c5': [SIM_ta_c5],
            'ta_c7': [SIM_ta_c7],
            'ta_c9': [SIM_ta_c9],
            'ta_c11': [SIM_ta_c11],
            'cqy_max_c7': [SIM_cqy_max_c7],
            'cqy_max_c8': [SIM_cqy_max_c8],
            'cqy_max_c9': [SIM_cqy_max_c9],
            'cqy_max_c12': [SIM_cqy_max_c12],
            'cqy_max_c18': [SIM_cqy_max_c18],
            'cqy_max_c19': [SIM_cqy_max_c19]            
            }) 
        df_records = pd.concat([df_records, dfts], ignore_index=True) # this adds the timestep dataframe to the historical values dataframe
        df_day_avg = df_records.groupby(['Day']).mean()
        df_day_sum = df_records.groupby(['Day']).sum()
        # advance timestep
        t += res                          
        pp_count += 1       # photoperiod counter + 1
    df_avg_sims = pd.concat([df_sims, df_day_avg], ignore_index=True) # this adds the timestep dataframe to the historical values dataframe
    df_sum_sims = pd.concat([df_sims, df_day_sum], ignore_index=True) # this adds the timestep dataframe to the historical values dataframe
    df_sims = df_avg_sims
    df_sims['DCG'] = df_sum_sims['DCG']
    df_sims['CGR'] = df_sum_sims['CGR']
    df_sims['DTR'] = df_sum_sims['DTR']

    # prints to console, which is captured as an HPC output
    print(df_sims.to_string(index=False, header=False))

# Executes this program/function
if __name__ == "__main__":
    # Parse command-line arguments
    args = sys.argv[1:]
    if len(args) != 32:
        print(f"Expected 32 arguments, but got {len(args)}")
        sys.exit(1)

    # Convert arguments to appropriate types
    SIM_NUM = int(args[0])
    params = list(map(float, args[1:]))

    # Call RUN_SIM with the parsed arguments
    RUN_SIM(SIM_NUM, *params)
