#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 20:06:45 2017

@author: FPCarneiro
"""

import pandas as pd
import tensorflow as tf

DATADIR = "input/"
#dtypes_train = {'id':'uint32', 'item_nbr':'int32', 'store_nbr':'int8', 'unit_sales':'float32'}
#dtypes_test = {'id':'uint32', 'item_nbr':'int32', 'store_nbr':'int8', 'unit_sales':'float32'}

stores = pd.read_csv("input/stores.csv")
items = pd.read_csv("input/items.csv")
oil = pd.read_csv("input/oil.csv", parse_dates=['date'], index_col='date')
transactions = pd.read_csv("input/transactions.csv", parse_dates=['date'])
holidays_events = pd.read_csv("input/holidays_events.csv", parse_dates=['date'])
sample_submission = pd.read_csv("input/sample_submission.csv", nrows=50)


def process_holidays(holidays):
    holidays['year'] = holidays['date'].dt.year
    relevant_fields = ['date', 'locale', 'locale_name', 'description','year']
    actual_dates = holidays[relevant_fields][holidays['type'] == 'Transfer'].rename(index=str, columns={"date": "actual_date"})
    actual_dates['description'] = actual_dates['description'].str.replace('Traslado ','').str.strip()
    
    holidays.drop(holidays[holidays['type'] == 'Transfer'].index, inplace=True)
    holidays = pd.merge(holidays, actual_dates, how='left', on=['locale','locale_name','description','year'])
    
    holidays.loc[pd.isnull(holidays['actual_date']), 'actual_date'] = holidays[pd.isnull(holidays['actual_date'])]['date']
    holidays = holidays.rename(index=str, columns={"date": "original_date"})
    holidays = holidays.rename(index=str, columns={"actual_date": "date"})
    return holidays


def loaddata(filename, 
             dtypes={'id':'uint32', 'item_nbr':'int32', 'store_nbr':'int8', 'unit_sales':'float32'}, 
             index_column=['id'], nrows=None):
    
    data = pd.read_csv(filename, parse_dates=['date'], 
                                     dtype=dtypes, nrows=nrows, index_col=index_column)
    
    data['onpromotion'].fillna(-1, inplace = True)
    data['onpromotion'] = data['onpromotion'].astype('int8')
    return data

def load_train_test_set():
    # From 2013-01-01 to 2017-08-15
    train = loaddata(DATADIR + "/train.csv", nrows=50000)
    # From 2017-08-16 to 2017-08-31 
    test = loaddata(DATADIR + "/test.csv", nrows=50000)
    return train, test

def load_stores(dtypes={'store_nbr':'int8', 'cluster': 'int32', 'store_nbr': 'int8'}):
    data = pd.read_csv(DATADIR + "/stores.csv", dtype = dtypes)
    return data

def load_holidays_events(dtypes={'transferred': bool}):
    data = process_holidays(pd.read_csv(DATADIR + "holidays_events.csv", parse_dates=['date']))
    return data

train, test = load_train_test_set()
stores = load_stores()
holidays_events = load_holidays_events()

def attach_stores(my_set, stores):
    attached_set = pd.merge(my_set, stores, how='left', on=['store_nbr'])
    return attached_set

def attach_holidays(my_set, holidays):
    
    def get_dummies(df):
        return df['type'].str.get_dummies('___')

    national = holidays[holidays['locale'] == 'National']
    national = pd.concat([national, get_dummies(national)], axis = 1)
    national['key'] = 0
    my_set['key'] = 0
    national = pd.merge(my_set, national, how='left', on=['key'])
    
    regional = holidays[holidays['locale'] == 'Regional']
    regional = pd.concat([regional, get_dummies(regional)], axis = 1)
    regional = pd.merge(my_set, regional, how='inner', left_on=['state'], right_on = ['locale_name'])
    
    local = holidays[holidays['locale'] == 'Local']
    local = pd.concat([local, get_dummies(local)], axis = 1)
    local = pd.merge(my_set, local, how='inner', left_on=['city'], right_on = ['locale_name'])

    return national, regional, local

def consolidate_holidays(my_set, holidays):
    n, r, l = attach_holidays(stores, holidays_events)
    n = n[['store_nbr', 'description', 'date', 'Additional', 'Bridge', 'Event', 'Holiday', 'Work Day']]
    r = r[['store_nbr', 'description', 'date', 'Holiday']]
    l = l[['store_nbr', 'description', 'date', 'Additional', 'Holiday']]

    res = pd.concat([n,r,l])
    res['Additional'].fillna(0, inplace = True)
    res['Bridge'].fillna(0, inplace = True)
    res['Event'].fillna(0, inplace = True)
    res['Holiday'].fillna(0, inplace = True)
    res['Work Day'].fillna(0, inplace = True)
    
    return res
    

train = attach_stores(train, stores)
resultado = consolidate_holidays(stores, holidays_events)
#oil.plot()

#del  stores, items, oil, sample_submission
#del test

train_25 = train.loc[(train['date'] == '2013-01-01') & (train['store_nbr'] == 25)]
transactions.loc[(transactions['date'] == '2013-01-01') & (transactions['store_nbr'] == 25)]
     
     
print("Nulls in Train columns: {0} => {1}".format(train.columns.values,train.isnull().any().values))
train.columns.values

###############################

item = tf.feature_column.numeric_column('item_nbr')
store = tf.feature_column.numeric_column('store_nbr')
sales = tf.feature_column.numeric_column('unit_sales')

train['onpromotion'].unique()



