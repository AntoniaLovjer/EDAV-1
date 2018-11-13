# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Notes
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
(*) This file contains all the functions needed to generate the running
    features out of the marathon splits
"""
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Imports
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
import pandas as pd
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Define the functions
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


def format_correctly(df):
    pd.DataFrame()

    # Subset the dataframe to only the relevant columns for this analysis
    split_cols = [col for col in df.columns if 'k' in col]
    other_cols = ['bib',
                  'name',
                  'official_time',
                  'pace_per_mile']
    total_cols = other_cols + split_cols
    output = df[total_cols]

    # Transform variables into DateTime
    for col in split_cols:
        df[col+'_min'] = pd.DatetimeIndex(df[col])
    return output
# ===========================================================================
