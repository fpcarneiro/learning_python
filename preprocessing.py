#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 21:01:45 2017

@author: FPCarneiro
"""

import pandas as pd

DATADIR = "input/"

def process_holidays(holidays):
    holidays['year'] = holidays['date'].dt.year
    relevant_fields = ['date', 'locale', 'locale_name', 'description','year']
    actual_dates = holidays[relevant_fields][holidays['type'] == 'Transfer'].rename(index=str, columns={"date": "actual_date"})
    actual_dates['description'] = actual_dates['description'].str.replace('Traslado ','').str.strip()
    
    holidays.drop(holidays[holidays['type'] == 'Transfer'].index, inplace=True)
    holidays = pd.merge(holidays, actual_dates, how='left', on=['locale','locale_name','description','year'])
    
    holidays.loc[pd.isnull(holidays['actual_date']), 'actual_date'] = holidays[pd.isnull(holidays['actual_date'])]['date']
    
    newcols = {"date": "original_date", 
            "actual_date": "date"}
    
    holidays.rename(columns=newcols, inplace=True)

    return holidays


def loaddata(filename, 
             dtypes={'id':'uint32', 'item_nbr':'int32', 'store_nbr':'int8', 'unit_sales':'float32'}, 
             index_column=None, nrows=None, skiprows=None):
    
    data = pd.read_csv(filename, parse_dates=['date'], 
                                     dtype=dtypes, nrows=nrows, index_col=index_column, skiprows=skiprows)
    
    data['onpromotion'].fillna(0, inplace = True)
    data['onpromotion'] = data['onpromotion'].astype('int8')
    
    data['year'] = data['date'].dt.year
    data['month'] = data['date'].dt.month
    data['day'] = data['date'].dt.day
    data['dow'] = data['date'].dt.dayofweek
    
    return data

def load_train_test_set():
    # From 2013-01-01 to 2017-08-15
    train = loaddata(DATADIR + "/train.csv", skiprows=range(1, 86672217), index_column=['id'])
    # From 2017-08-16 to 2017-08-31 
    test = loaddata(DATADIR + "/test.csv")
    return train, test

def load_stores(dtypes={'store_nbr':'int8', 'cluster': 'int8', 'city': str, 'state': str, 'type': str}):
    data = pd.read_csv(DATADIR + "/stores.csv", dtype = dtypes)
    return data

def load_holidays_events(dtypes={'transferred': bool}):
    data = process_holidays(pd.read_csv(DATADIR + "holidays_events.csv", parse_dates=['date'], dtype=dtypes))
    return data

def load_items(dtypes={'item_nbr':'int32', 'class':'int32', 'perishable': 'int8'}):
    data = pd.read_csv(DATADIR + "items.csv", dtype=dtypes)
    return data

def attach_stores(my_set, stores):
    attached_set = pd.merge(my_set, stores, how='left', on=['store_nbr'])
    return attached_set

def attach_items(my_set, items):
    attached_set = pd.merge(my_set, items, how='left', on=['item_nbr'])
    return attached_set

def attach_holidays(my_set, holidays):
    
    def get_dummies(df):
        return df['type'].str.get_dummies('___')

    national = holidays[holidays['locale'] == 'National']
    national = pd.concat([national, get_dummies(national)], axis = 1)
    national['key'] = 0
    my_set['key'] = 0
    national = pd.merge(my_set, national, how='left', on=['key'], suffixes=['_store','_holiday'])
    
    regional = holidays[holidays['locale'] == 'Regional']
    regional = pd.concat([regional, get_dummies(regional)], axis = 1)
    regional = pd.merge(my_set, regional, how='inner', left_on=['state'], right_on = ['locale_name'], suffixes=['_store','_holiday'])
    
    local = holidays[holidays['locale'] == 'Local']
    local = pd.concat([local, get_dummies(local)], axis = 1)
    local = pd.merge(my_set, local, how='inner', left_on=['city'], right_on = ['locale_name'], suffixes=['_store','_holiday'])

    return national, regional, local

def consolidate_holidays(my_set, holidays):
    n, r, l = attach_holidays(my_set, holidays)
    n = n[['store_nbr', 'description', 'date', 'locale', 'Additional', 'Bridge', 'Event', 'Holiday', 'Work Day']]   
    r = r[['store_nbr', 'description', 'date', 'locale', 'Holiday']]
    l = l[['store_nbr', 'description', 'date', 'locale', 'Additional', 'Holiday']]

    res = pd.concat([n,r,l])
    res['Additional'].fillna(0, inplace = True)
    res['Bridge'].fillna(0, inplace = True)
    res['Event'].fillna(0, inplace = True)
    res['Holiday'].fillna(0, inplace = True)
    res['Work Day'].fillna(0, inplace = True)
    
    res[['Holiday', 'Additional','Bridge','Event','Work Day']] = res[['Holiday', 'Additional','Bridge','Event','Work Day']].astype('int8')
    
    return res
    
def attach_holidays_in_stores(my_set, store_holidays):
    df = pd.merge(my_set, store_holidays, how='left', on = ['store_nbr', 'date'])
    df['Additional'].fillna(0, inplace = True)
    df['Bridge'].fillna(0, inplace = True)
    df['Event'].fillna(0, inplace = True)
    df['Holiday'].fillna(0, inplace = True)
    df['Work Day'].fillna(0, inplace = True)
    df['description'].fillna(-1, inplace = True)
    df['locale'].fillna(-1, inplace = True)
    
    df[['Holiday', 'Additional','Bridge','Event','Work Day']] = df[['Holiday', 'Additional','Bridge','Event','Work Day']].astype('int8')
    df = df.rename(index=str, columns={"Work Day": "Work_Day"})
    return df

def adjust_unit_sales(my_set):
    my_set.loc[(my_set.unit_sales < 0),'unit_sales'] = 0
    my_set['unit_sales'] = my_set['unit_sales'].apply(pd.np.log1p)
    return my_set

def load_all():
    train, test = load_train_test_set()
    stores = load_stores()
    holidays_events = load_holidays_events()
    items = load_items()
    
    #oil = pd.read_csv("input/oil.csv", parse_dates=['date'], index_col='date')
    #transactions = pd.read_csv("input/transactions.csv", parse_dates=['date'])
    #sample_submission = pd.read_csv("input/sample_submission.csv", nrows=50)
    
    return train, test, stores, holidays_events, items