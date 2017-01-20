#!/usr/bin/env python

"""
These are some useful data management functions
"""

#========================================================================
# Import what you need
#========================================================================
import numpy as np
import pandas as pd

#========================================================================
def read_in_behavdata(behav_data_f):
    """
    This function reads in the ABIDE phenotypic data file,
    removes all participants who have no measure in the
    func_perc_fd column or if they have no associated
    connectivity matrix file ('FILE_ID' variable).

    It also calculates and adds a variable called AGE_YRS
    which is the age of the participant in years.

    Finally the function removes all participants who are
    younger than 6 and older than 18 and returns
    the pandas data frame.
    """
    df = pd.read_csv(behav_data_f)
    df = df.loc[df['func_perc_fd'].notnull(), :]
    df = df.loc[df['FILE_ID']!='no_filename', :]
    df['AGE_YRS'] = np.floor(df['AGE_AT_SCAN'])
    df= df.loc[(df['AGE_YRS']>=6)& (df['AGE_YRS']<=18), :] #only include kids

    return df

#========================================================================
def filter_data(df, motion_thresh, age_l, age_u, motion_measure='func_perc_fd'):
    """
    This function filters the data so you're looking at data
    within a certain age range (between age_l and age_u *inclusive*)
    and with particpants who have motion lower than a certain
    value of motion_measure (set to func_perc_fd by default but
    an alternative value would be func_mean_fd.
    """
    # Start by removing all participants whose data is below a certain
    # motion threshold.
    df_samp_motion =  df.loc[df[motion_measure] < motion_thresh, :]

    # Then remove participants who are younger (in years) than age_l and older
    # than age_u. Note that this means people who are age_l and age_u
    # (eg 6 and 10) will be included in the sample.
    df_samp = df_samp_motion.loc[(df_samp_motion['AGE_YRS']>=age_l)
                                  & (df_samp_motion['AGE_YRS']<=age_u), :]

    return df_samp

#========================================================================
def select_random_sample(df, n=100):
    """
    This function shuffles the data in filtered_df and then selects
    the top n entries.
    """
    # Make a copy (just because sometimes crazy things happen when you
    # shuffle in python!)
    df_copy = df.copy()

    # Permute the data and re-index
    df_copy = df_copy.reindex(np.random.permutation(df_copy.index))

    # Then just take the top n
    df_copy = df_copy.iloc[:n, :]

    return df_copy
    
