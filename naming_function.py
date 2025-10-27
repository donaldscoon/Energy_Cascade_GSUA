"""
Naming Functions of the MEC GSUA(s)

Author: Donald Coon
Date: January 2025

Description: 
This is a collection of functions used throughout the MEC GSUA(s). 
They assisst in managing the GSUA problem statement, provide 
a single place to alter names/labels of inputs and outputs and
serves as a location to define user paths.

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


import os
from SALib import ProblemSpec

def prob_spec(GSUA_type, inputs):
    """
    Define the parameter specifications for the General Sensitivity and Uncertainty Analysis (GSUA).

    This function provides a central location for all the parameters of the MEC versions 
    used in the GSUA. Depending on the type of GSUA needed, it sets up a problem specification 
    with parameter names, bounds, distributions, and outputs.

    Parameters
    ----------
    GSUA_type : str
        Specifies the type of GSUA to be performed. Different types dictate different parameter setups.
    inputs : any
        Additional input parameters, not currently used in the function.

    Returns
    -------
    ProblemSpec
        An instance of ProblemSpec configured with the names, number of variables, bounds, 
        distributions, and outputs according to the specified GSUA type for use with SALib.


    Examples
    --------
    To run a specific GSUA configuration:
    >>> sp = prob_spec(GSUA_type='XXXX', inputs=None)
    """
    
    # For parameters stated in literature as a single value a uniform distribution 
    # is assigned ranging from that value +- 20%.
    plus        = 1.2 # upper bound of uniform distributions
    minus       = 0.8 # lower bound of uniform distributions

    dist_TEMP   = [19,23]                   # Cav 2004 range of temp that the MEC is parameterized for 
    dist_RH     = [75*minus,75*plus] 
    dist_CO2    = [330,1320]                # Ewert Table 4-123 lettuce values
    dist_PPFD   = [200,500]                 # Cavazzoni 2004, range of possible values
    dist_H      = [16*minus,16*plus]        # Ewert Table 4-111
    dist_P_ATM  = [101*minus,101*plus]      # Gainesville, Florida, USA, Atmo pressure
    dist_BCF    = [0.40*minus,0.4*plus]     # Ewert table 4-113 
    dist_XFRT   = [0.95*minus,1]            # Ewert table 4-112 assumed 1 is the maximum value
    dist_OPF    = [1.08*minus,1.08*plus]    # Ewert Table 4-113
    dist_g_A    = [2.5*minus,2.5*plus]      # Ewert Equation 4-27
    dist_A_MAX  = [0.93*minus,1*plus]       # Cavazzoni 2004, upper bound limited to not exceed 1 
    dist_t_E    = [1,5]                                             # Ewert Table 4-112 says 1, +- a percentage wouldn't makes sense
    dist_CQY_min= [0,0.2]                                           # Ewert Table 4-99 Technically n/a for lettuce
    dist_CUE_max= [0.625*minus,0.625*plus]                          # Ewert table 4-99
    dist_CUE_min= [0,0.2]                                           # Ewert Table 4-99 technically n/a for lettuce
    dist_D_PG   = [24*minus,24*plus]                                # Boscheri 
    dist_n      = [2.5*minus,2.5*plus]                              # Ewert table 4-97
    dist_DRY_FR = [(6.57/131.35)*minus,(6.57/131.35)*plus]          # Hanford 2004 Table 4.2.7, with part from wheeler 2003
    dist_NC_FR  = [0.034*minus,0.034*plus]                          # Hanford 2004 table 4.2.10
    dist_ta_c2  = [(1.0289*(10**4))*minus,(1.0289*(10**4))*plus]    # Ewert Table 4-115
    dist_ta_c3  = [-3.7018*plus,-3.7018*minus]                      # Ewert Table 4-115
    dist_ta_c5  = [(3.6648*(10**-7))*minus,(3.6648*(10**-7))*plus]  # Ewert Table 4-115
    dist_ta_c7  = [1.7571*minus,1.7571*plus]                        # Ewert Table 4-115
    dist_ta_c9  = [(2.3127*(10**-6))*minus,(2.3127*(10**-6))*plus]  # Ewert Table 4-115
    dist_ta_c11 = [(1.876)*minus,(1.876)*plus]                      # Ewert Table 4-115
    dist_cqy_max_c7 = [(4.4763*(10**-2))*minus,(4.4763*(10**-2))*plus]          # Ewert Table 4-102
    dist_cqy_max_c8 = [(5.163*(10**-5))*minus,(5.163*(10**-5))*plus]            # Ewert Table 4-102
    dist_cqy_max_c9 = [(-2.075*(10**-8))*plus,(-2.075*(10**-8))*minus]          # Ewert Table 4-102
    dist_cqy_max_c12= [(-1.1701*(10**-5))*plus,(-1.1701*(10**-5))*minus]        # Ewert Table 4-102
    dist_cqy_max_c18= [(-1.9731*(10**-11))*plus,(-1.9731*(10**-11))*minus]      # Ewert Table 4-102
    dist_cqy_max_c19= [(8.9265*(10**-15))*minus,(8.9265*(10**-15))*plus]        # Ewert Table 4-102
    dist_t_Mi = [16*minus, 16*plus]                                             # initial time of maturity (days) Amitrano 2020 table 2
    dist_amin_GN = [0.00691867456539118*minus, 0.00691867456539118*plus]        # amitrano 2020 calibrated with growth chamber experiment exact value from her data
    dist_amin_GON =[0.00342717997911672*minus, 0.00342717997911672*plus]        # amitrano 2020 calibrated with growth chamber experiment exact value from her data
    dist_amax_GN = [0.017148682744336*minus, 0.017148682744336*plus]            # amitrano 2020 calibrated with growth chamber experiment exact value from her data
    dist_amax_GON =[0.00952341360955465*minus, 0.00952341360955465*plus]        # amitrano 2020 calibrated with growth chamber experiment exact value from her data
    dist_bmin_GN = [0*minus, 0.03]                                              # amitrano 2020 calibrated with growth chamber experiment exact value from her data, upper bound estimated
    dist_bmin_GON =[0.0486455477321762*minus, 0.0486455477321762*plus]          # amitrano 2020 calibrated with growth chamber experiment exact value from her data
    dist_bmax_GN = [0.0451765692503675*minus, 0.0451765692503675*plus]          # amitrano 2020 calibrated with growth chamber experiment exact value from her data
    dist_bmax_GON =[0.0564626043274799*minus, 0.0564626043274799*plus]          # amitrano 2020 calibrated with growth chamber experiment exact value from her data
    dist_K = [0.098*minus,0.098*plus]               # Volk et al. 1995 table 2 
    dist_C = [0.57*minus, 0.68]                     # This range is close to the 0.57+-20% as maximum CUE would be 0.68 from M. W. Van Iersel, “Carbon use efficiency depends on growth respiration, maintenance respiration, and relative growth rate. A case study with lettuce,” Plant Cell & Environment, vol. 26, no. 9, pp. 1441–1449, Sep. 2003, doi: 10.1046/j.0016-8025.2003.01067.x.
    dist_t_a = [22*minus,22*plus]                   # Estimate of t_a for lettuce that aligns with nominal expiremental results
    dist_t_m = [30*minus,30*plus]                   # aligns with AMI's t_Mi
    dist_Q_min = [0.0125*minus,0.0125*plus]         # Volk et al. 1995 Table 3
    dist_Q_max = [0.054*minus,0.054*plus]           # Volk et al. 1995 Table 3 is 0.0625 this value is based on experimental results from CAV and BOS

    # Problem Specification for the Cavazzoni GSUA
    if GSUA_type == 'CAV_expanded': 
        sp = ProblemSpec({
            'names': ['T_LIGHT', 'RH', 'CO2', 'PPFD', 'H', 'P_ATM', 'BCF', 'XFRT', 'OPF', 'g_A', 'A_MAX',
                      't_E', 'CQY_MIN', 'CUE_MIN', 'CUE_MAX', 'n', 'ta_c2', 'ta_c3', 'ta_c5', 'ta_c7', 'ta_c9', 'ta_c11',
                      'cqy_max_c7', 'cqy_max_c8', 'cqy_max_c9', 'cqy_max_c12', 'cqy_max_c18', 'cqy_max_c19'],
            'num_vars': 28,
            'bounds': [dist_TEMP, dist_RH, dist_CO2, dist_PPFD, dist_H, dist_P_ATM, dist_BCF, dist_XFRT, 
                       dist_OPF, dist_g_A, dist_A_MAX, dist_t_E, dist_CQY_min, dist_CUE_min, dist_CUE_max,
                       dist_n, dist_ta_c2, dist_ta_c3, dist_ta_c5, dist_ta_c7, dist_ta_c9, dist_ta_c11, 
                       dist_cqy_max_c7, dist_cqy_max_c8, dist_cqy_max_c9, dist_cqy_max_c12, dist_cqy_max_c18, 
                       dist_cqy_max_c19],
            'dists': ['unif','unif','unif','unif','unif','unif','unif','unif','unif','unif',
                      'unif','unif','unif','unif','unif','unif','unif','unif','unif','unif',
                      'unif','unif','unif','unif','unif','unif','unif','unif'],
            'outputs': ['Y']
        })

    # Problem Specification for the Boscheri GSUA
    elif GSUA_type == 'BOS_expanded':
        sp = ProblemSpec({
            'names': ['T_LIGHT', 'RH', 'CO2', 'PPFD', 'H', 'P_ATM', 'BCF', 'XFRT', 'OPF', 'g_A', 'A_MAX',
                      't_E', 'CQY_MIN', 'CUE_MAX', 'CUE_MIN', 'D_PG', 'n', 'DRY_FR', 'DRY_NC_FR', 'ta_c2', 
                      'ta_c3', 'ta_c5', 'ta_c7', 'ta_c9', 'ta_c11', 'cqy_max_c7', 'cqy_max_c8', 'cqy_max_c9',
                      'cqy_max_c12', 'cqy_max_c18', 'cqy_max_c19'],
            'num_vars': 31,
            'bounds': [dist_TEMP, dist_RH, dist_CO2, dist_PPFD, dist_H, dist_P_ATM, dist_BCF, dist_XFRT, 
                       dist_OPF, dist_g_A, dist_A_MAX, dist_t_E, dist_CQY_min, dist_CUE_max, dist_CUE_min, 
                       dist_D_PG, dist_n, dist_DRY_FR, dist_NC_FR, dist_ta_c2, dist_ta_c3, dist_ta_c5, 
                       dist_ta_c7, dist_ta_c9, dist_ta_c11, dist_cqy_max_c7, dist_cqy_max_c8, dist_cqy_max_c9, 
                       dist_cqy_max_c12, dist_cqy_max_c18, dist_cqy_max_c19],
            'dists': ['unif','unif','unif','unif','unif','unif','unif','unif','unif','unif',
                      'unif','unif','unif','unif','unif','unif','unif','unif','unif','unif',
                      'unif','unif','unif','unif','unif','unif','unif','unif','unif', 'unif',
                      'unif'],
            'outputs': ['Y']
        })

    # Problem Specification for the Amitrano GSUA
    elif GSUA_type == 'AMI_expanded': 
        sp = ProblemSpec({
            'names': ['TEMP', 'RH', 'CO2', 'PPFD', 'H', 'P_ATM', 'BCF', 'XFRT', 'OPF', 'g_A', 't_E', 't_Mi',
                      'amin_GN', 'amax_GN', 'bmin_GN', 'bmax_GN', 'amin_GON', 'amax_GON', 'bmin_GON', 'bmax_GON'],
            'num_vars': 20,
            'bounds': [dist_TEMP, dist_RH, dist_CO2, dist_PPFD, dist_H , dist_P_ATM, dist_BCF, 
                       dist_XFRT, dist_OPF, dist_g_A, dist_t_E, dist_t_Mi, dist_amin_GN, dist_amax_GN, dist_bmin_GN,
                       dist_bmax_GN, dist_amin_GON, dist_amax_GON, dist_bmin_GON, dist_bmax_GON],
            'dists': ['unif','unif','unif','unif','unif','unif','unif','unif','unif','unif',
                      'unif','unif','unif','unif','unif','unif','unif','unif','unif', 'unif'],
            'outputs': ['Y']
        })

    # Problem Specification for the Volk GSUA
    elif GSUA_type == 'Energy_Cascade':
        sp = ProblemSpec({            
            'names': ['PPFD', 'H', 'K', 'C', 't_a', 't_m', 'A_MAX', 'Q_min', 'Q_max'],
            'num_vars': 9,
            'bounds': [dist_PPFD, dist_H , dist_K, dist_C, dist_t_a, dist_t_m, dist_A_MAX, dist_Q_min, dist_Q_max],
            'dists': ['unif','unif','unif','unif','unif','unif','unif','unif','unif'],
            'outputs': ['Y']})
    return sp

def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def ensure_file_exists(file_path):
    ensure_directory_exists(os.path.dirname(file_path))
    with open(file_path, 'a'):
        os.utime(file_path, None)

def path_names():
    """
    Defines and returns the file paths used for storing and retrieving GSUA results.

    This function provides a centralized location for defining various folder paths used 
    in the GSUA process. The paths include locations for general storage, individual 
    GSUA results. The paths need to be adjusted according to the user's environment 
    (Local and HPC).

    Returns
    -------
    tuple
        A tuple containing the following paths:
        - gen_path: The highest-level folder of the program (str).
        - indiv_path: The location of the results for the individual GSUA's (str).
        - structure_path: an unused remenant of development (str).
        - AMI_BLUE_PATH: Storage area for specific HiPerGator resources (str).
        - BOS_BLUE_PATH: Storage area for specific HiPerGator resources (str).
        - CAV_BLUE_PATH: Storage area for specific HiPerGator resources (str).

    Notes
    -----
    Make sure to adjust these folder paths according to your specific environment:
    - Local paths
    - HPC paths

    The Volk EC model, which was added late in development uses its 
    own standalone version of this function.

    Examples
    --------
    To get the path names for storing GSUA results:
    >>> gen_path, indiv_path, structure_path, AMI_BLUE_PATH, BOS_BLUE_PATH, CAV_BLUE_PATH = path_names()
    """
    
    ##### HOME PATHS
    gen_path =      '[YOUR PATH HERE]'
    indiv_path =    '[YOUR PATH HERE]'
    structure_path ='[YOUR PATH HERE]'

    ##### HPC Paths
    AMI_BLUE_PATH = '[YOUR PATH HERE]'
    BOS_BLUE_PATH = '[YOUR PATH HERE]'
    CAV_BLUE_PATH = '[YOUR PATH HERE]'

    return gen_path, indiv_path, structure_path, AMI_BLUE_PATH, BOS_BLUE_PATH, CAV_BLUE_PATH

def EC_info():
    """
    Define and return the configuration information for the Energy Cascade (EC) system.

    This function provides a centralized location for defining various configuration 
    settings used in the Energy Cascade (EC) model. These settings include general 
    paths for storing results, specific paths for HPC resources, and the type 
    of General Sensitivity and Uncertainty Analysis (GSUA) being performed.

    Returns
    -------
    tuple
        A tuple containing the following information:
        - gen_path: The highest-level folder of the program for individual GSUA results (str).
        - EC_BLUE_PATH: Storage area for specific HPC resources related to EC (str).
        - GSUA_type: Specifies the type of GSUA to be performed (str).

    Notes
    -----
    Make sure to adjust these folder paths according to your specific environment.

    Examples
    --------
    To get the EC configuration information:
    >>> gen_path, EC_BLUE_PATH, GSUA_type = EC_info()
    """

def model_names(): 
    models = [
            ["AMI", "Amitrano"], 
            ["BOS", "Boscheri"], 
            ["CAV", "Cavazzoni"]
            ]
    return models

def mec_input_names(GSUA_type):
    """
    Define and return the names and attributes of MEC inputs for GSUA.

    This function provides a list of variable names, long names, units, 
    formatted names, and charting colors for the inputs used in different 
    types of General Sensitivity and Uncertainty Analysis (GSUA). The variable names 
    and attributes are adjusted according to the specified GSUA type.

    Parameters
    ----------
    GSUA_type : str
        Specifies the type of GSUA to be performed. Different types dictate 
        different lists of input variables.

    Returns
    -------
    list of list
        A list of lists where each inner list contains:
        - Variable Name (str)
        - Long Name (str)
        - Units (str)
        - Formatted Name (str)
        - Charting Color (str)

    Notes
    -----
    The unicode for the micro symbol is used for some variable units.

    Examples
    --------
    To get the MEC input names for a specific GSUA type:
    >>> mec_inputs = mec_input_names(GSUA_type='XXXX')
    """

    u = "\u00B5"        # unicode for the micro symbol
    if GSUA_type == 'CAV_expanded':
        mec_inputs = [
            # ['Variable Name', 'long name', 'units', 'formatted name', 'charting color]
            ["T_LIGHT", "Light Cycle Temperature", "Degrees Celsius", "T$_{LIGHT}$", "#004c6d"],
            ["T_DARK", "Dark Cycle Temperature", "Degrees Celsius", "T$_{DARK}$", "#377290"],
            ["RH", "Relative Humidity", "%", "RH", "#609ab4"],
            ["CO2", "CO$_{2}$ Concentration", u+"mol$_{carbon}$ mol$_{air}$", "CO$_{2}$", "#8ac4d9"],
            ["PPFD", "Photosynthetic Photon Flux", u+"mol$_{photons}$ m$^{-2}$ second$^{-1}$", "PPFD", "#b6efff"],
            ["H", "Photoperiod", "hours day$^{-1}$", "H", "#88011b"],
            ["P_ATM", "Atmospheric Pressure", "kPa", "P$_{ATM}$", "#a94542"],
            ["BCF", "Biomass Carbon Fraction", "%", "BCF", "#c8756e"],
            ["XFRT", "Edible Biomass Fration", "%", "XFRT", "#e5a59d"],
            ["OPF", "Oxygen Production Fraction", "Fractional", "OPF", "#ffd6d0"],
            ["g_A", "Atmospheric Conductance", "mol$_{water}$m$^{-2}$ second$^{-1}$", "g$_{A}$", "#4a6fe3"],
            ["A_MAX", "Maximum Absorpance", "", "A$_{MAX}$", "#788beb"],
            # ["t_Q", "Time of Canopy Senescence", "days"],
            ["t_E", "Time of Organ Formation", "days", "t$_{E}$", "#9ea8f2"],
            ["CQY_MIN", "Minimum CQY", u+"mol$_{fixed}$ "+u+"mol$_{aborbed}$", "CQY$_{MIN}$", "#c0c5f9"],
            ["CUE_MIN", "Minimum CUE", "", "CUE$_{MIN}$", "#e2e4ff"],
            ["CUE_MAX", "Maximum CQY", "", "CUE$_{MAX}$", "#db9a3e"],
            ["n", "Crop specific exponent", "", "n", "#e7b266"],
            ["ta_c2", "t_A coefficient", "", "ta$_{C2}$", "#d33f6a"],
            ["ta_c3", "t_A coefficient", "", "ta$_{C3}$", "#e16989"],
            ["ta_c5", "t_A coefficient", "", "ta$_{C5}$", "#ed8ea7"],
            ["ta_c7", "t_A coefficient", "", "ta$_{C7}$", "#f7b2c4"],
            ["ta_c11", "t_A coefficient", "", "ta$_{C11}$", "#ffd5e1"],
            ["cqy_max_c7", "CQY_max coefficient", "", "CQY$_{MAXC7}$", "#0d952a"],
            ["cqy_max_c8", "CQY_max coefficient", "", "CQY$_{MAXC8}$", "#50ac51"],
            ["cqy_max_c9", "CQY_max coefficient", "", "CQY$_{MAXC9}$", "#7bc477"],
            ["cqy_max_c12", "CQY_max coefficient", "", "CQY$_{MAXC12}$", "#a3db9e"],
            ["cqy_max_c18", "CQY_max coefficient", "", "CQY$_{MAXC18}$", "#caf3c5"],
            ["cqy_max_c19", "CQY_max coefficient", "", "CQY$_{MAXC19}$", "#cd8207"]
            ]

    elif GSUA_type == 'BOS_expanded':
        mec_inputs = [
            # ['Variable Name', 'long name', 'units', 'formatted name', 'charting color]
            ["T_LIGHT", "Light Cycle Temperature", "Degrees Celsius", "T$_{LIGHT}$", "#004c6d"],
            ["T_DARK", "Dark Cycle Temperature", "Degrees Celsius", "T$_{DARK}$", "#377290"],
            ["RH", "Relative Humidity", "%", "RH", "#609ab4"],
            ["CO2", "CO$_{2}$ Concentration", u+"mol$_{carbon}$ mol$_{air}$", "CO$_{2}$", "#8ac4d9"],
            ["PPFD", "Photosynthetic Photon Flux", u+"mol$_{photons}$ m$^{-2}$ second$^{-1}$", "PPFD", "#b6efff"],
            ["H", "Photoperiod", "hours day$^{-1}$", "H", "#88011b"],
            ["P_ATM", "Atmospheric Pressure", "kPa", "P$_{ATM}$", "#a94542"],
            ["BCF", "Biomass Carbon Fraction", "%", "BCF", "#c8756e"],
            ["XFRT", "Edible Biomass Fration", "%", "XFRT", "#e5a59d"],
            ["OPF", "Oxygen Production Fraction", "Fractional", "OPF", "#ffd6d0"],
            ["g_A", "Atmospheric Conductance", "mol$_{water}$m$^{-2}$ second$^{-1}$", "g$_{A}$", "#4a6fe3"],
            ["A_MAX", "Maximum Absorpance", "", "A$_{MAX}$", "#788beb"],
            # ["t_Q", "Time of Canopy Senescence", "days"],
            ["t_E", "Time of Organ Formation", "days", "t$_{E}$", "#9ea8f2"],
            ["CQY_MIN", "Minimum CQY", u+"mol$_{fixed}$ "+u+"mol$_{aborbed}$", "CQY$_{MIN}$", "#c0c5f9"],
            ["CUE_MIN", "Minimum CUE", "", "CUE$_{MIN}$", "#e2e4ff"],
            ["CUE_MAX", "Maximum CQY", "", "CUE$_{MAX}$", "#db9a3e"],
            ["D_PG", "Crop Diurnal Cycle", "hours", "D$_{PG}$", "#f4c98e"],
            ["n", "Crop specific exponent", "", "n", "#e7b266"],
            ["DRY_FR", "Dry over wet biomass", "g$_{dry}$ g$_{wet}$$^{-1}$", "DRY$_{FR}$", "#ffe1b6"],
            ["NC_FR", "Nutrient Consumption", "g$_{nutrients}g$^{-1}$ $_{biomass}$", "NC$_{FR}$", "#0a867c"],
            ["ta_c2", "t_A coefficient", "", "ta$_{C2}$", "#d33f6a"],
            ["ta_c3", "t_A coefficient", "", "ta$_{C3}$", "#e16989"],
            ["ta_c5", "t_A coefficient", "", "ta$_{C5}$", "#ed8ea7"],
            ["ta_c7", "t_A coefficient", "", "ta$_{C7}$", "#f7b2c4"],
            ["ta_c11", "t_A coefficient", "", "ta$_{C11}$", "#ffd5e1"],
            ["cqy_max_c7", "CQY_max coefficient", "", "CQY$_{MAXC7}$", "#0d952a"],
            ["cqy_max_c8", "CQY_max coefficient", "", "CQY$_{MAXC8}$", "#50ac51"],
            ["cqy_max_c9", "CQY_max coefficient", "", "CQY$_{MAXC9}$", "#7bc477"],
            ["cqy_max_c12", "CQY_max coefficient", "", "CQY$_{MAXC12}$", "#a3db9e"],
            ["cqy_max_c18", "CQY_max coefficient", "", "CQY$_{MAXC18}$", "#caf3c5"],
            ["cqy_max_c19", "CQY_max coefficient", "", "CQY$_{MAXC19}$", "#cd8207"]
            ]

    elif GSUA_type == 'AMI_expanded':
        mec_inputs = [
            # ['Variable Name', 'long name', 'units', 'formatted name']
            ["T_LIGHT", "Light Cycle Temperature", "Degrees Celsius", "T$_{LIGHT}$", "#004c6d"],
            ["RH", "Relative Humidity", "%", "RH", "#609ab4"],
            ["CO2", "CO$_{2}$ Concentration", u+"mol$_{carbon}$ mol$_{air}$", "CO$_{2}$", "#8ac4d9"],
            ["PPFD", "Photosynthetic Photon Flux", u+"mol$_{photons}$ m$^{-2}$ second$^{-1}$", "PPFD", "#b6efff"],
            ["H", "Photoperiod", "hours day$^{-1}$", "H", "#88011b"],
            ["P_ATM", "Atmospheric Pressure", "kPa", "P$_{ATM}$", "#a94542"],
            ["BCF", "Biomass Carbon Fraction", "%", "BCF", "#c8756e"],
            ["XFRT", "Edible Biomass Fration", "%", "XFRT", "#e5a59d"],
            ["OPF", "Oxygen Production Fraction", "Fractional", "OPF", "#ffd6d0"],
            ["g_A", "Atmospheric Conductance", "mol$_{water}$m$^{-2}$ second$^{-1}$", "g$_{A}$", "#4a6fe3"],
            ["t_E", "Time of Organ Formation", "days", "t$_{E}$", "#9ea8f2"],
            ["t_Mi", "time of maturity", "days", "t$_{Mi}$", "#3ea197"],
            ["amin_GN", "crop specific constant", "", "$\\alpha$$_{MIN}$GN", "#61bdb2"],
            ["amax_GN", "crop specific constant", "", "$\\alpha$$_{MAX}$GN", "#82dacf"],
            ["bmin_GN", "crop specific constant", "", "$\\beta$$_{MIN}$GN", "#a3f7ec"],
            ["bmax_GN", "crop specific constant", "", "$\\beta$$_{MAX}$GN", "#a2668b"],
            ["amin_GON", "crop specific constant", "", "$\\alpha$$_{MIN}$GON", "#b981a6"],
            ["amax_GON", "crop specific constant", "", "$\\alpha$$_{MAX}$GON", "#d09dc2"],
            ["bmin_GON", "crop specific constant", "", "$\\beta$$_{MIN}$GON", "#e7bade"],
            ["bmax_GON", "crop specific constant", "", "$\\beta$$_{MAX}$GON", "#ffd7fa"]
        ]

    elif GSUA_type == 'Energy_Cascade':
        mec_inputs = [
            # ['Variable Name', 'long name', 'units', 'formatted name']
            ["PPFD", "Photosynthetic Photon Flux", u+"mol$_{photons}$ m$^{-2}$ second$^{-1}$", "PPFD", "#b6efff"],
            ["H", "Photoperiod", "hours day$^{-1}$", "H", "#88011b"],
            ["K", "Conversion Constant", "", "K", "#696939"],
            ["C", "Carbon Use Effeciency", "", "C", "#888753"],
            ["t_a", "Time of Canopy Closure", "days", "t$_{A}$", "#a8a76d"],
            ["t_m", "Time of Crop maturity", "days", "t$_{M}$", "#3ea197"],
            ["A_MAX", "Maximum Absorpance", "", "A$_{MAX}$", "#788beb"],
            ["Q_min", "Minimum Canopy Quantum Yield", "mol$_{fixed}$ / "+"mol$_{aborbed}$", "Q$_{MIN}$", "#c9c789"],
            ["Q_max", "Minimum Canopy Quantum Yield", "mol$_{fixed}$ / "+"mol$_{aborbed}$", "Q$_{MAX}$", "#ebe9a6"],
        ]    

    return mec_inputs

def mec_output_names():
    """
    Define and return the names and attributes of MEC outputs.

    This function provides a list of output variable names, long names, units, 
    and formatted names for the outputs of the General Sensitivity and Uncertainty 
    Analysis (GSUA). The variable names and attributes are used for easy reference 
    and visualization in charts and reports.

    Returns
    -------
    list of list
        A list of lists where each inner list contains:
        - Output Short Name (str)
        - Output Long Name (str)
        - Output Units (str)
        - Output Formatted Name (str)

    Notes
    -----
    The unicode for the micro symbol is used for some variable units.

    Examples
    --------
    To get the MEC output names:
    >>> outputs = mec_output_names()
    """

    u = "\u00B5"        # unicode for the micro symbol
    outputs = [  
        # ['output short name', 'output long name', 'output units', 'output formatted name']
        ["A", "Absorption", "", "A"],
        ["CQY", "Canopy Quantum Yield", u+"mol$_{fixed}$ "+u+"mol$_{aborbed}$", "CQY"],
        ["CUE_24", "Carbon Use Efficiency", "", "CUE$_{24}$"],
        ["DCG", "Daily Carbon Gain", "mol$_{carbon}$ m$^{-2}$ day$^{-1}$", "DCG"],
        ["CGR", "Crop Growth Rate", "grams m$^{-2}$ day$^{-1}$", "CGR"],
        ["TCB", "Total Crop Biomass", "grams m$^{-2}$", "TCB"],
        ["TEB", "Total Edible Biomass", "grams m$^{-2}$", "TEB"],
        ["VP_SAT", "Saturated Moisture Vapor Pressure", "kPa", "VP$_{SAT}$"],
        ["VP_AIR", "Actual Moisture Vapor Pressure", "kPa", "VP$_{AIR}$"],
        ["VPD", "Vapor Pressure Deficit", "kPa", "VPD"],
        ["P_GROSS", "Gross Canopy Photosynthesis", u+"mol$_{carbon}$ m$^{-2}$ second$^{-1}$", "P$_{GROSS}$"],
        ["P_NET", "Net Canopy Photosynthesis", u+"mol$_{carbon}$ m$^{-2}$ second$^{-1}$", "P$_{NET}$"],
        ["g_S", "Stomatal Conductance", "mol$_{water}$ m$^{-2}$ second$^{-1}$", "g$_{S}$"],
        ["g_A", "Atmospheric Conductance", "mol$_{water}$ m$^{-2}$ second$^{-1}$", "g$_{A}$"],
        ["g_C", "Canopy Conductance", "mol$_{water}$ m$^{-2}$ second$^{-1}$", "g$_{C}$"],
        ["DTR", "Daily Transpiration Rate", "L$_{water}$ m$^{-2}$ day$^{-1}$", "DTR"]
        ]
    return outputs

def colors(): 
    # Model, dark color, light color, med/bright color, marker
    colors = [['AMI', '#2A119B', '#A798EC', '#5E46C6', 'o'],     # blues
              ['BOS', '#067300', '#96F391', '#09B600', 's'],     # greens
              ['CAV', '#8C0004', '#FE989A', '#DF0006', '^']]    # reds

def df_labels():
    df_AMI_sims_label = ['Timestep','???','SIM_NUM', 'H','A','ALPHA','BETA','CQY','CUE_24',
                        'DCG','CGR','TCB','TEB','DOP','VP_SAT','VP_AIR','VPD','P_GROSS',
                        'P_NET','g_S','g_A','g_C','DTR','T_LIGHT','T_DARK','RH','CO2','PPFD', 'STRU']

    df_BOS_sims_label = ['SIM_NUM','Timestep','H','Diurnal', 'A','ALPHA','BETA','CQY',
                        'CUE_24','DCG','CGR','DWCGR','TCB','TEB',
                        'VP_SAT','VP_AIR','VPD','P_NET','P_GROSS',
                        'DOP','DOC','g_S','g_A','g_C','DTR',
                        'DCO2C','DCO2P','DNC', 'DWC','T_LIGHT',
                        'T_DARK','RH','CO2','PPFD', 'STRU']

    df_CAV_sims_label = ['SIM_NUM','Timestep','H','A','ALPHA','BETA','CQY','CUE_24','DCG',
                        'CGR','TCB','TEB','DOP','VP_SAT','VP_AIR','VPD','P_GROSS',
                        'P_NET','g_S','g_A','g_C','DTR','T_LIGHT','T_DARK','RH','CO2','PPFD', 'STRU']


    return df_AMI_sims_label, df_BOS_sims_label, df_CAV_sims_label

def sobol_EE_labels(GSUA_type):
    if GSUA_type == "CAV_expanded":
        ST_S1_Label = ['TEMP', 'RH', 'CO2', 'PPFD', 'H', 'P_ATM', 'BCF', 'XFRT', 'OPF', 'g_A', 'A_MAX',
                       't_E', 'CQY_MIN', 'CUE_MAX', 'CUE_MIN', 'n', 'ta_c2', 'ta_c3', 'ta_c5', 'ta_c7', 'ta_c9', 'ta_c11',
                       'cqy_max_c7', 'cqy_max_c8', 'cqy_max_c9', 'cqy_max_c12', 'cqy_max_c18', 'cqy_max_c19']

    elif GSUA_type == "BOS_expanded":
        ST_S1_Label = ['TEMP', 'RH', 'CO2', 'PPFD', 'H', 'P_ATM', 'BCF', 'XFRT', 'OPF', 'g_A', 'A_MAX',
                       't_E', 'CQY_MIN', 'CUE_MIN', 'CUE_MAX', 'D_PG', 'n', 'DRY_FR', 'NC_FR', 'ta_c2', 'ta_c3', 
                       'ta_c5', 'ta_c7', 'ta_c9', 'ta_c11', 'cqy_max_c7', 'cqy_max_c8', 'cqy_max_c9', 
                       'cqy_max_c12', 'cqy_max_c18', 'cqy_max_c19']
 
    elif GSUA_type == "AMI_expanded":
        ST_S1_Label = ['TEMP', 'RH', 'CO2', 'PPFD', 'H', 'P_ATM', 'BCF', 'XFRT', 'OPF', 'g_A', 't_E', 't_Mi',
                       'amin_GN', 'amax_GN', 'bmin_GN', 'bmax_GN', 'amin_GON', 'amax_GON', 'bmin_GON', 'bmax_GON']

    elif GSUA_type == "Energy_Cascade":
        ST_S1_Label = ['PPFD', 'H', 'K', 'C', 't_a', 't_m', 'A_MAX', 'Q_min', 'Q_max']
        
    S2_label = []

    # Iterates through the ST_S1_Label to generate the matching index for S2
    for i in ST_S1_Label:
        for j in ST_S1_Label:
            S2_label.append(f'{i}x{j}')

    return ST_S1_Label, S2_label 

def conf_bars():
    elinewidth = .75
    capsize = 2
    capthick = .75

    return elinewidth, capsize, capthick

def sobol_colors():
    # https://graphicdesign.stackexchange.com/questions/3682/where-can-i-find-a-large-palette-set-of-contrasting-colors-for-coloring-many-d
    # plus 5 additionalto cover the full range
    sobol_colors = ["#023fa5", "#7d87b9", "#bec1d4", "#d6bcc0", "#bb7784", 
                    "#8e063b", "#4a6fe3", "#8595e1", "#b5bbe3", "#e6afb9", 
                    "#e07b91", "#d33f6a", "#11c638", "#8dd593", "#c6dec7", 
                    "#ead3c6", "#f0b98d", "#ef9708", "#0fcfc0", "#9cded6", 
                    "#d5eae7", "#f3e1eb", "#f6c4e1", "#f79cd4", 
                    '#7a5195', '#ef5675', '#ffa600', '#003f5c', '#ffa07a ']
    return sobol_colors
