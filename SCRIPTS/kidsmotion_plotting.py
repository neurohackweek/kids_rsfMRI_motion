#!/usr/bin/env python

"""
Here are some useful plotting functions!
"""

#===============================================================================
# Import what you need
#===============================================================================
import matplotlib.pylab as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import pandas as pd
import seaborn as sns

#===============================================================================
def get_min_max(data, pad=0.05):
    """
    This function finds the minimum and maximum values for the data and then
    pads values by pad (in fractional values, set to 5% as default) of the data
    so you can have a little bit of space around the values in your plot.
    """
    data_range = np.max(data) - np.min(data)
    data_min = np.min(data) - (data_range * pad)
    data_max = np.max(data) + (data_range * pad)

    return data_min, data_max

#===============================================================================
def histogram_motion(df):
    """
    This function plots histograms of the func_mean_fd and func_perc_md values
    for all participants in a data frame along with a scatter plot of these
    two motion measures against each other.

    Returns the fig and ax_list
    """
    fig, ax_list = plt.subplots(1,3, figsize=(9,3))
    ax_list[0] = sns.distplot(df['func_mean_fd'], ax=ax_list[0])
    xmin, xmax = get_min_max(df['func_mean_fd'])
    ax_list[0].set_xlim(xmin, xmax)

    ax_list[1] = sns.distplot(df['func_perc_fd'], ax=ax_list[1])
    xmin, xmax = get_min_max(df['func_perc_fd'])
    ax_list[1].set_xlim(xmin, xmax)

    ax_list[2] = sns.regplot(df['func_mean_fd'], df['func_perc_fd'], fit_reg=False, scatter_kws={'s': 3}, ax=ax_list[2])
    xmin, xmax = get_min_max(df['func_mean_fd'])
    ymin, ymax = get_min_max(df['func_perc_fd'])
    ax_list[2].set_xlim(xmin, xmax)
    ax_list[2].set_ylim(ymin, ymax)

    for ax in ax_list:
        ax.xaxis.set_major_locator(MaxNLocator(5))
        ax.yaxis.set_major_locator(MaxNLocator(5))

    sns.despine()
    plt.tight_layout()

    return fig, ax_list


#===============================================================================
def corr_motion_age(df, fit_reg=True):
    """
    This function correlates age and motion (both func_mean_fd and func_perc_md)
    for all participants in a data frame.

    Returns the fig and ax_list
    """
    fig, ax_list = plt.subplots(1,2, figsize=(6,3))

    for i, motion_measure in enumerate([ 'func_mean_fd', 'func_perc_fd']):
        ax_list[i] = sns.regplot(df['AGE_AT_SCAN'], df[motion_measure],
                                    fit_reg=fit_reg,
                                    scatter_kws={'s': 3}, ax=ax_list[i])
        xmin, xmax = get_min_max(df['AGE_AT_SCAN'])
        ymin, ymax = get_min_max(df[motion_measure])
        ax_list[i].set_xlim(xmin, xmax)
        ax_list[i].set_ylim(ymin, ymax)

    for ax in ax_list:
        ax.xaxis.set_major_locator(MaxNLocator(5))
        ax.yaxis.set_major_locator(MaxNLocator(5))

    sns.despine()
    plt.tight_layout()

    return fig, ax_list

#===============================================================================
def compare_groups_boxplots(corr_df, title=None):
    """
    This function plots the output of the compare_groups function (which
    doesn't exist yet) as swarm and boxplots showing the correlation with a
    particular variable.

    corr_df is made up of rows contains the r values from a number of permutations and columns defined according to different ways of selecting
    the groups.
    """
    fig, ax = plt.subplots(figsize=(5,3))
    ax = sns.boxplot(data=corr_df,
                        orient='v',
                        ax=ax,
                        linewidth=2,
                        color='w',
                        width=0.5)
    ax = sns.swarmplot(data=corr_df,
                        orient='v',
                        ax=ax,
                        s=2)
    ax.axhline(c='k', lw=0.5, ls='--')
    sns.despine()

    if title:
        ax.text(0.95, 0.95, title,
                horizontalalignment='right',
                verticalalignment='bottom',
                transform = ax.transAxes)

    # Make the plot look pretty by limiting the numbmer of ticks on the
    # yaxis
    ax.yaxis.set_major_locator(MaxNLocator(5))

    plt.tight_layout()

    return fig, ax
