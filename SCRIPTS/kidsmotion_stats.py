#!/usr/bin/env python

"""
Here are some useful stats functions!
"""

#========================================================================
# Import what you need
#========================================================================
import numpy as np
from scipy.stats import ttest_1samp, pearsonr
from statsmodels.sandbox.stats.multicomp import fdrcorrection0 as fdr
import pandas as pd

#========================================================================

def regional_ttest(df, cols_list):

    # Create a list of t and p values
    # and the mean and standard deviations
    # for each region
    t_list = []
    p_list = []
    mean_list = []
    std_list = []
    stars_list = []

    # Now loop through these regions
    for col in cols_list:

        # Save the mean and standard deviation values
        mean_list += [df.loc[df[col].notnull(), col].mean()]
        std_list += [df.loc[df[col].notnull(), col].std()]

        # Conduct the t-test regionally
        t, p = ttest_1samp(df.loc[df[col].notnull(), col], 0)
        t_list += [t]
        p_list += [p]

        # Get a "star" value for this test so you can print it nicely
        # NOTE that these are not corrected
        star = 'ns'
        if p < 0.05:
            star = '*'
        if p < 0.01:
            star = '**'
        if p < 0.001:
            star = '***'

        stars_list += [star]

    # Calculate the fdr corrected p values
    fdr_mask, fdr_ps = fdr(np.array(p_list))

    # Turn these values into a dictionary
    ttest_dict = { 'regions' : cols_list,
                   'means'   : np.array(mean_list),
                   'stds'    : np.array(std_list),
                   'ts'      : np.array(t_list),
                   'ps'      : np.array(p_list),
                   'fdr_ps'  : np.array(fdr_ps),
                   'stars'   : np.array(stars_list)}

    return ttest_dict

#========================================================================
def calculate_correlation(df, x_name, y_name, covar_name=None):
    """
    This function prints r and p values for a correlation.

    It takes as input a data frame and two strings representing
    the x and y variables. These strings (x_name and y_name) must be
    columns in the data frame (df).

    If covar_name is presented then this command corrects for (just one
    at the moment) covariate and then calcaultes the partial correlation.

    P values are always reported to 3 decimal places, the r_dp argument
    controls how many decimal places to report the r value to.
    """
    if not covar_name:
        r, p = pearsonr(df[x_name], df[y_name])

    else:
        x_res = residuals(df[covar_name], df[x_name])
        y_res = residuals(df[covar_name], df[y_name])

        df['{}_res'.format(x_name)] = x_res
        df['{}_res'.format(y_name)] = y_res

        r, p = pearsonr(df['{}_res'.format(x_name)], df['{}_res'.format(y_name)])

    return r, p


def report_correlation(df, x_name, y_name, covar_name=None, r_dp=2):
    """
    This function prints r and p values for a correlation.

    It takes as input a data frame and two strings representing
    the x and y variables. These strings (x_name and y_name) must be
    columns in the data frame (df).

    If covar_name is presented then this command corrects for (just one
    at the moment) covariate and then calcaultes the partial correlation.

    P values are always reported to 3 decimal places, the r_dp argument
    controls how many decimal places to report the r value to.
    """
    # Calculate the correlation
    r, p = calculate_correlation(df, x_name, y_name, covar_name=covar_name)

    # Format nicely
    r, p = format_r_p(r, p, r_dp=r_dp)

    print('    r {}, p {}'.format(r, p))

#========================================================================
def format_r_p(r, p, r_dp=2):
    """
    This function formats r and p to make them look really nice for
    printing to screen.
    """
    r = '{:2.{width}f}'.format(r, width=r_dp)
    r = '= {}'.format(r)

    if p < 0.001:
        p = '< .001'
    else:
        p = '{:2.3f}'.format(p)
        p = '= {}'.format(p[1:])

    return r, p

#========================================================================
def residuals(x, y):
    '''
    A useful little function that correlates
    x and y together to give their residual
    values. These can then be used to calculate
    partial correlation values.
    '''
    import numpy as np

    if len(x.shape) == 1:
        x = x[np.newaxis, :]
    A = np.vstack([x, np.ones(x.shape[-1])]).T
    B = np.linalg.lstsq(A, y)[0]
    m = B[:-1]
    c = B[-1]
    pre = np.sum(m * x.T, axis=1) + c
    res = y - pre
    return res
