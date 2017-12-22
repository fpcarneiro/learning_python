#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 20:06:45 2017
@author: FPCarneiro
"""

import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split

DATADIR = "input/"
MODELDIR = "model/"
#dtypes_train = {'id':'uint32', 'item_nbr':'int32', 'store_nbr':'int8', 'unit_sales':'float32'}
#dtypes_test = {'id':'uint32', 'item_nbr':'int32', 'store_nbr':'int8', 'unit_sales':'float32'}

#stores = pd.read_csv("input/stores.csv")
items = pd.read_csv("input/items.csv")
oil = pd.read_csv("input/oil.csv", parse_dates=['date'], index_col='date')
transactions = pd.read_csv("input/transactions.csv", parse_dates=['date'])
#holidays_events = pd.read_csv("input/holidays_events.csv", parse_dates=['date'])
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
    
    data['onpromotion'].fillna(0, inplace = True)
    data['onpromotion'] = data['onpromotion'].astype('int8')
    return data

def load_train_test_set():
    # From 2013-01-01 to 2017-08-15
    train = loaddata(DATADIR + "/train.csv", nrows=50000)
    # From 2017-08-16 to 2017-08-31 
    test = loaddata(DATADIR + "/test.csv", nrows=50000)
    return train, test

def load_stores(dtypes={'store_nbr':'int8', 'cluster': 'int8', 'city': str, 'state': str, 'type': str}):
    data = pd.read_csv(DATADIR + "/stores.csv", dtype = dtypes)
    return data

def load_holidays_events(dtypes={'transferred': bool}):
    data = process_holidays(pd.read_csv(DATADIR + "holidays_events.csv", parse_dates=['date']))
    return data

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
    national = pd.merge(my_set, national, how='left', on=['key'], suffixes=['_store','_holiday'])
    
    regional = holidays[holidays['locale'] == 'Regional']
    regional = pd.concat([regional, get_dummies(regional)], axis = 1)
    regional = pd.merge(my_set, regional, how='inner', left_on=['state'], right_on = ['locale_name'], suffixes=['_store','_holiday'])
    
    local = holidays[holidays['locale'] == 'Local']
    local = pd.concat([local, get_dummies(local)], axis = 1)
    local = pd.merge(my_set, local, how='inner', left_on=['city'], right_on = ['locale_name'], suffixes=['_store','_holiday'])

    return national, regional, local

def consolidate_holidays(my_set, holidays):
    n, r, l = attach_holidays(stores, holidays_events)
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
    
train, test = load_train_test_set()
stores = load_stores()
holidays_events = load_holidays_events()

train = attach_stores(train, stores)
stores_holidays = consolidate_holidays(stores, holidays_events)

train = attach_holidays_in_stores(train, stores_holidays)


#oil.plot()

#del  stores, items, oil, sample_submission
#del x_data

train_25 = train.loc[(train['date'] == '2013-01-01') & (train['store_nbr'] == 25)]
transactions.loc[(transactions['date'] == '2013-01-01') & (transactions['store_nbr'] == 25)]
     
     
print("Nulls in Train columns: {0} => {1}".format(train.columns.values,train.isnull().any().values))
train.columns.values
train['onpromotion'].unique()
######################################################################################################################################

#item = tf.feature_column.numeric_column('item_nbr')
sales = tf.feature_column.numeric_column('unit_sales')

store_type = tf.feature_column.categorical_column_with_vocabulary_list('type', ['A', 'B', 'C', 'D', 'E'])

additional = tf.feature_column.categorical_column_with_vocabulary_list('Additional', [0,1])
bridge = tf.feature_column.categorical_column_with_vocabulary_list('Bridge', [0,1])
event = tf.feature_column.categorical_column_with_vocabulary_list('Event', [0,1])
holiday = tf.feature_column.categorical_column_with_vocabulary_list('Holiday', [0,1])
work_day = tf.feature_column.categorical_column_with_vocabulary_list('Work_Day', [0,1])
onpromotion = tf.feature_column.categorical_column_with_vocabulary_list('onpromotion', [0,1], dtype=tf.int8)

store_cluster = tf.feature_column.categorical_column_with_vocabulary_list(key='cluster', vocabulary_list=list(range(1,18)), dtype=tf.int32)

store_city = tf.feature_column.categorical_column_with_hash_bucket('city', hash_bucket_size=22)
store_state = tf.feature_column.categorical_column_with_hash_bucket('state', hash_bucket_size=16)
store_nbr = tf.feature_column.categorical_column_with_hash_bucket('store_nbr', hash_bucket_size=54, dtype=tf.int8)
item_nbr = tf.feature_column.categorical_column_with_hash_bucket('item_nbr', hash_bucket_size=4100, dtype=tf.int32)

########################################################################################################################################

base_columns = [store_type, additional, bridge, event, holiday, work_day, 
                onpromotion, store_cluster, store_city, store_state, store_nbr, item_nbr]

base_columns = [store_nbr, item_nbr, onpromotion, store_city, store_state, store_type, store_cluster]
                
crossed_columns = [tf.feature_column.crossed_column([onpromotion, holiday], hash_bucket_size=4)]

x = train.drop(['unit_sales', 'date'], axis = 1)
y = train['unit_sales']

model = tf.estimator.LinearRegressor(model_dir=MODELDIR, feature_columns = base_columns)

input_func = tf.estimator.inputs.pandas_input_fn(x = x, y = y, batch_size = 128, num_epochs = None, shuffle = True)
train_input_func = tf.estimator.inputs.pandas_input_fn(x = x, y = y, batch_size = 128, num_epochs = 1000, shuffle = False)
#eval_input_func = tf.estimator.inputs.pandas_input_fn(x = x_eval, y = y_eval, batch_size = 8, num_epoch = 1000, shuffle = False)


model.train(input_fn=input_func, steps = 1000)
