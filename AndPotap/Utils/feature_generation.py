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
import re
import time
import pandas as pd
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Define the functions
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


def format_correctly(df, verbose=False):
    """
    Properly formats the DateTime objects and introduces inplace
    the DateTime objects columns in seconds
    :param df: DataFrame | the marathon DataFrame
    :param verbose: bool | True prints the time the function took
    :return: DataFrame | the original DataFrame with the
                            extra columns
    """
    t0 = time.time()

    # Focus on the relevant columns
    split_cols = [col for col in df.columns if 'k' in col]

    # Transform variables into DateTime
    for col in split_cols:

        # Generate new column
        new_col = col + '_sec'
        # km = int(re.findall(r'\d+', col)[0])

        # Introduce the DateTime objects
        aux = pd.DatetimeIndex(df[col])
        df[col] = aux

        # Subset for non NaTs
        mask = pd.notnull(aux)

        df.loc[mask, new_col] = (aux[mask].hour * 3600 +
                                 aux[mask].minute * 60 +
                                 aux[mask].second)

    rename_cols = {'splint_5k_sec': 'sec_1',
                   'splint_10k_sec': 'sec_2',
                   'splint_15k_sec': 'sec_3',
                   'splint_20k_sec': 'sec_4',
                   'splint_25k_sec': 'sec_5',
                   'splint_30k_sec': 'sec_6',
                   'splint_35k_sec': 'sec_7',
                   'splint_40k_sec': 'sec_8'}

    rename_cols_2 = {'splint_5k': '5k_1',
                     'splint_10k': '10k_2',
                     'splint_15k': '15k_3',
                     'splint_20k': '20k_4',
                     'splint_25k': '25k_5',
                     'splint_30k': '30k_6',
                     'splint_35k': '35k_7',
                     'splint_40k': '40k_8'}

    df = df.rename(columns=rename_cols)

    df = df.rename(columns=rename_cols_2)

    df['ID'] = df.index

    t1 = time.time()
    if verbose:
        print('\nFormatting took: {:6.1f} sec'.format(t1 - t0))

    return df


def subset_columns(columns):
    """
    Subsets a given list of columns to the ones matching
    the ('\d+') RegEx pattern
    :param columns: pd.Index | index of a given DataFrame
    :return: list | a list containing matching elements
    """
    subset = []
    for col in columns:
        if len(re.findall(r'_\d+', string=col)) > 0:
            subset.append(col)
    return subset


def give_difference(total_columns, columns):
    """
    Returns the difference between two given sets of columns
    :param total_columns: pd.Index | index of the whole data set
    :param columns: list | a subset list of columns from total
    :return: list | the columns not contained in the subset
    """
    a = set(total_columns)
    b = set(columns)
    c = a.difference(b)
    return list(sorted(c))


def add_diffs(df, verbose=False):
    """
    Adds the features that contain the differences in seconds
    between the marathon 5 k splits
    :param df: DataFrame | the marathon DataFrame
    :param verbose: bool | True prints the time the function took
    :return: DataFrame | the original DataFrame with
                            the extra columns
    """
    t0 = time.time()
    col_diffs = ['sec_1',
                 'sec_2',
                 'sec_3',
                 'sec_4',
                 'sec_5',
                 'sec_6',
                 'sec_7',
                 'sec_8']

    df.loc[:, 'pace_total'] = df.loc[:, col_diffs[-1]] / len(col_diffs)

    df.loc[:, 'diff_1'] = df[col_diffs[0]]

    df.loc[:, 'pace_1'] = df[col_diffs[0]] / df['pace_total']

    df.loc[:, 'pace_index_1'] = 100

    for i in range(len(col_diffs) - 1):

        # Name new columns
        new_col_diff = 'diff_' + str(i + 2)
        new_col_pace = 'pace_' + str(i + 2)
        new_col_pace_index = 'pace_index_' + str(i + 2)

        # Introduce the new data
        df.loc[:, new_col_diff] = (df[col_diffs[i + 1]] -
                                   df[col_diffs[i]])

        df.loc[:, new_col_pace] = df[new_col_diff] / df['pace_total']

        df.loc[:, new_col_pace_index] = 100 * (df[new_col_diff] /
                                               df[col_diffs[0]])

    t1 = time.time()
    if verbose:
        print('\nConstructing diffs took: {:6.1f} sec'.format(t1 - t0))

    return df


def reshape_properly(df, verbose=False):
    """
    Augments the DataFrame by a factor of 8 in order
    to incorporate the analysis at a marathon split level
    :param df: DataFrame | the raw marathon data
    :param verbose: bool | True prints the time the function took
    :return: DataFrame | the augmented DataFrame
    """
    t0 = time.time()
    aux = df.copy()

    other = subset_columns(columns=df.columns)
    id_vars = give_difference(total_columns=df.columns,
                              columns=other)

    # Melt for some columns (this is placeholder)
    selected = [col for col in df.columns if 'k' in col]
    df_placeholder = pd.melt(frame=aux, id_vars=id_vars,
                             value_vars=selected)
    df_placeholder.loc[:, 'ID_R'] = (df_placeholder['ID'].apply(str) + '_'
                                     + df_placeholder['variable'].str.get(-1))

    # Melt for all the columns
    aux = pd.melt(frame=aux, id_vars=id_vars)

    aux.loc[:, 'ID_R'] = (aux['ID'].apply(str) + '_'
                          + aux['variable'].str.get(-1))

    aux.loc[:, 'identifier'] = 'NaN'

    mask = aux['variable'].str.contains('k')
    aux.loc[mask, 'identifier'] = 'date_time'

    mask = aux['variable'].str.contains('sec_')
    aux.loc[mask, 'identifier'] = 'sec'

    mask = aux['variable'].str.contains('diff_')
    aux.loc[mask, 'identifier'] = 'diff'

    mask = aux['variable'].str.contains('pace_')
    aux.loc[mask, 'identifier'] = 'pace'

    mask = aux['variable'].str.contains('pace_index')
    aux.loc[mask, 'identifier'] = 'pace_index'

    id_q = aux['identifier'].unique()

    df_total = pd.DataFrame(index=aux['ID_R'].unique())
    df_total['ID_R'] = df_total.index
    df_total = df_total.reset_index(drop=True)
    for identifier in id_q:
        tmp = aux[aux['identifier'] == identifier].copy()
        tmp = tmp[['ID_R', 'identifier', 'value']]
        tmp = tmp.set_index('ID_R')
        tmp = tmp.pivot(columns='identifier', values='value')

        df_total = pd.merge(left=df_total,
                            right=tmp,
                            how='inner',
                            on='ID_R')

    # Revert back the columns
    df_placeholder = pd.merge(left=df_placeholder,
                              right=df_total,
                              how='inner',
                              on='ID_R')

    t1 = time.time()
    if verbose:
        print('\nAugmenting the data took: {:6.1f} sec'.format(t1 - t0))

    return df_placeholder
# ===========================================================================
