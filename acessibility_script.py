# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 13:20:14 2014@author: mdowd
A function to calculate accessibiility from a each zone to some a

"""

data = r"C:\Users\mdo\Desktop\autott2851.csv"
access_unit = r"C:\Users\mdo\Desktop\pop_taz.csv"

def access(matrix, matrix_label, access_unit, access_label, cutoff, decay_not_limit=True, decay_lambda = 0.05, diagnols=False):
    """
    ________
    Packages necessary: Pandas, numpy
    ________
    
    matrix: must be a travel matrix in csv format.
        <<<<>>>>>
    matrix_label: is whatever value is found in the upper left most corner of the matrix above.
        <<<<>>>>>    
    access_unit: must be csv table, it can have multiple fields. This should be something like a table of
        of various zonal information.
        <<<<>>>>>    
    access_label: this is the Column Name of the access measue you are interested in.
        <<<<>>>>>    
    cutoff: This is a value whereby all areas below the cutoff have full access to access_units
        in other words if the cutoff is 30 minutes, then any zone that can be reached in 30 minutes
         from another zone will be considered to have full access to that access unit. 
        <<<<>>>>>
    decay_not_limt: If decay_not_limit is true then a decay function is applied over the cutoff value, if
        decay_not_limit = False then all access)units accessiblie within a certain time limit are added and
        all units not accessiblit within that time are ignored. 
        DEFAULT = True
    decay_lambda = the value that is used in the decay function that is applied for travel values over the
        cutoff value: Decay Function = Access_Unit * exp(Travel_Time * -decay_lambda5)
        DEFAULT = 0.05
        <<<<>>>>>
    diagnols: True if you want diagnol values set to zero, false if you want to include the intrazonal
        access to access_unts. 
        DEFAULT = False

    """
    from math import exp
    import numpy as np
    from pandas import DataFrame, read_csv, read_excel
    import pandas as pd
    
    #Prepare Data 
    #read the travel matrix skim into a --> dataframe
    df = read_csv(data).drop(matrix_label,axis=1)
    #convert travel matriz skim dataframe to --> matrix
    dmatrix = df.as_matrix()
    
    #Read in the "accessibility measure" could be persons, jobs, firms, needs to be a zonal total
    #based on the zonal unit. ie. total jobs per taz, function will return access to jobs by taz
    access_data = read_csv(access_unit)
    vector = np.array(access_data[access_label])

    ###Start by making a boolean array for your condition.
    mask = dmatrix > cutoff

    ##Create Output
    output = np.ones(dmatrix.shape)*vector

    ###Now use mask to selectively assign the result of the conditional operation
    exp_function = output[mask]*np.exp(dmatrix[mask]*-decay_lambda)
    gamma_function = (output[mask]/vector.sum()) * (dmatrix[mask]**-0.503) * np.exp(-0.078*dmatrix[mask])
    
    if decay_not_limit:
        output[mask] = gamma_function
    else:
        output[mask] = output[mask]*0

    ###Removing Diagnols means a zone loses access to its own "Accessibility Measure", I think it make
    ## more sense to keep the intrazonal access
    if diagnols:
        di = np.diag_indices(len(dmatrix))
        output[di] = 0

    ##Fix the 2728-2851 cells since we don't know anything about them
    out_df = DataFrame(output, columns = [i for i in xrange(1,len(output)+1)], index = [i for i in xrange(1,len(output)+1)])
    return out_df, out_df.sum(axis=1)
    
    ##Example Call to function
    access(r"C:\Users\mdo\Desktop\autott2851.csv",'TIMEAUTO',r"C:\Users\mdo\Desktop\pop_taz.csv", \
    'POP100_RE', 30 ,decay_not_limit = True, decay_lambda = 0.005, diagnols=True )
    