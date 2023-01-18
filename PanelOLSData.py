#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""
    Name: PanelOLSData
    
    Purpose: Create a panel dataframe in a usable format to tools such as PanelOLS from multiple
             input files
    
    Version    Date          Description
    V1.0:      01/17/2023    Initial release
"""


# In[ ]:


import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')


# In[ ]:


"""
    Inputs:
            - new_data: df to be added or formated
            - axis: 'x' for dfs with years arranged in columns, 'y' o.w.
            - countrycol_name, yearcol_name, targetcol_name: names of respective columns in new_data
            - dataset: optional paramenter used when you want to add to an existing output
    Outputs:
            - new_dataset: df formated and/or merged with new data
"""
def append_data(new_data, axis, countrycol_name, yearcol_name, targetcol_name, dataset = pd.DataFrame()):
    miss_countries = []
    if len(dataset) != 0:
        new_dataset = dataset
        new_dataset[targetcol_name] = np.nan
    else:
        print('Starting new dataset...')
        new_dataset = pd.DataFrame()
        countries = [country for country in new_data[countrycol_name].unique()]
        if axis == 'x':
            years = [year for year in new_data.columns if str(year).isnumeric()]
        elif axis == 'y':
            years = [year for year in new_data[yearcol_name].unique()]
        i = 0
        for country in countries:
            for year in years:
                new_dataset.loc[i, 'country'] = country
                new_dataset.loc[i, 'year'] = year
                i += 1
    for country in new_dataset['country'].unique():
        for year in new_dataset['year'].unique():
            index = new_dataset[new_dataset.year == year][new_dataset.country == country].index
            if axis == 'x':
                new_data_filt = new_data[new_data[countrycol_name] == country]
                if len(new_data_filt) > 0:
                    new_data_filt = new_data_filt[str(int(year))]
                    new_dataset.loc[index, targetcol_name] = new_data_filt[new_data_filt.index[0]]
                else: miss_countries.append(country)
            elif axis == 'y':
                new_data_filt = new_data[new_data[countrycol_name] == country][new_data[yearcol_name] == year]
                if len(new_data_filt) > 0:
                    new_dataset.loc[index, targetcol_name] = new_data_filt[targetcol_name][new_data_filt.index[0]]
                else: miss_countries.append(country)
        print('-', end = '')
    print('\nThere were missed samples in due to names miss matching or missing years in the ' + 
          'following countries:\n' + str(set(miss_countries)))
    return new_dataset

"""
    Inputs:
            - data_df: df with country names or codes in a column
            - countrycol: countries column name
            - codetype: 'Alpha-2 code', 'Alpha-3 code' or 'Numeric'
    Outputs:
            - merged_df: df formated and/or merged with new data
"""
def add_countrycol(data_df, countrycol, codetype, countrycodes_df):
    for code_type in countrycodes_df.columns:
        if codetype in code_type:
            data_df = data_df.rename(columns={countrycol: code_type})
            merged_df = pd.merge(data_df, countrycodes_df, on=[code_type])
            return merged_df
    return 'Wrong call'


# In[ ]:




