#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 20:06:45 2017
@author: FPCarneiro
"""

MODELDIR = "model/"

import gc
import pandas as pd
import tensorflow as tf
#from sklearn.model_selection import train_test_split

import preprocessing as pp
import train_tensor_flow as ttf

train, test, stores, holidays_events, items = pp.load_all()

stores_holidays = pp.consolidate_holidays(stores, holidays_events)

train = pp.adjust_unit_sales(train)

train = pp.attach_stores(train, stores)
train = pp.attach_holidays_in_stores(train, stores_holidays)
train = pp.attach_items(train, items)

test = pp.attach_stores(test, stores)
test = pp.attach_holidays_in_stores(test, stores_holidays)
test = pp.attach_items(test, items)

del stores, holidays_events, items

gc.collect()

x = train.drop(['unit_sales', 'date', 'description', 'locale', 'year'], axis = 1)
y = train['unit_sales']

del train
gc.collect()

x_eval = test.drop(['date', 'description', 'locale', 'year', 'id'], axis = 1)

# TENSOR FLOW LINEAR REGRESSION ###############################################################################################

base_columns = ttf.get_base_columns()

model = tf.estimator.LinearRegressor(model_dir=ttf.MODELDIR, feature_columns = base_columns)

input_func = tf.estimator.inputs.pandas_input_fn(x = x, y = y, batch_size = 1024, num_epochs = None, shuffle = True)
train_input_func = tf.estimator.inputs.pandas_input_fn(x = x, y = y, batch_size = 1024, num_epochs = 1000, shuffle = False)
predict_input_func = tf.estimator.inputs.pandas_input_fn(x = x_eval, shuffle = False)

model.train(input_fn=input_func, steps = 1000)

train_metrics = model.evaluate(input_fn = train_input_func, steps = 1000)

predict_results = model.predict(input_fn = predict_input_func)

pred = [pd.np.expm1(i['predictions'][0]) for i in predict_results]

se = pd.Series(pred)
test['unit_sales'] = se.values


test[['id','unit_sales']].to_csv('sub0.csv.gz', index=False, float_format='%.3f', compression='gzip')

#50% more for promotion items
test.loc[test['onpromotion'] == True, 'unit_sales'] *= 1.5  
        
test[['id','unit_sales']].to_csv('sub1.csv.gz', index=False, float_format='%.3f', compression='gzip')
