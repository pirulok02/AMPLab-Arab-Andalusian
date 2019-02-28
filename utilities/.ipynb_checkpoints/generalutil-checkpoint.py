import pandas as pd
import numpy as np

def get_cols_df(df,cols=[]):
    return df[cols]

def rem_cols_df(df,cols=[]):
    colidx = set(df.columns.tolist())-cols
    return df[colidx]

def remove_items_with_empty_cells(df):
    return df.replace(to_replace = '',value = np.nan).dropna(how = 'any',axis = 0)
        