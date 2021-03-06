import numpy as np
import pandas as pd
import tensorflow as tf
from pandas import ExcelWriter
import openpyxl
import datetime
from clustering.som import SOM
from DataTools import DataReformat as datarf
from model import reformat
import random


#-----------------------------------Data pre-process-------------------------------------------------------
# get  training data
df = pd.read_excel('./data/WPG_data.xlsx')

# -----------------------------------input data random pre-process------------------------------------
df_ran = df.sample(frac=1)

# define which title to be noimal
df_nominal = df_ran.ix[:, ['Report Date', 'Customer', 'Type','Item Short Name', 'Brand', 'Sales']]
df_numerical_tmp = df_ran.ix[:,:]
df_numerical = df_numerical_tmp.apply(pd.to_numeric, errors='coerce').fillna(-1)


# get data dim to latter SOM prcess
input_dim = len(df_numerical.columns)
input_num = len(df_numerical.index)


# -----------------------------------input data random pre-process------------------------------------
# change data to np array (SOM accept nparray format)
input_data = np.array(df_numerical)


#-----------------------------------SOM process-------------------------------------------------------

#Train a 20x30 SOM with 400 iterations
som = SOM(30, 20, input_dim, input_data, input_num)
print('training start : ' + str(datetime.datetime.now()))
som.train(input_data)


#Map datato their closest neurons
mapped = som.map_vects(input_data)
result = np.array(mapped)

print(result)
# -------------------------check each data belong to which cluster---------------------------------------
clusting_result_location_list = datarf.clustered_location_input_index(5, 5, result, input_data)
print(clusting_result_location_list)

#-------------------------------------Output format-----------------------------------------------------
# output format
output_np = np.concatenate((df_nominal, result), axis=1)
output_pd = pd.DataFrame(data=output_np, columns=['Report Date', 'Customer', 'Type', 'Item Short Name', 'Brand', 'Sales', 'axis-x', 'axis-y'])
# print(output_pd)




# write to final csv
output_pd.to_csv('./result/result_final.csv')