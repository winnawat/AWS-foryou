"""
Script that trains a simply perceptron using the keras library on the MNIST
dataset.  This script is used as a test for the AWS_foryou algo_runner function.
"""

import numpy as np
import pandas as pd
#from keras.models import Sequential
#from keras.layers import Dense
#from keras.layers import Dropout
#from keras.utils import np_utils

import sys
import time

import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

import importlib

def algo_runner(python_call, moduleName):

    # locate the data and target locations

    data_loc_len = len('data_loc=')
    data_loc_loc = python_call.find('data_loc=')
    location_1 = data_loc_loc + data_loc_len
    comma_loc = python_call.find(',')

    target_loc_len = len('target_loc=')
    target_loc_loc = python_call.find('target_loc=')
    location_2 = target_loc_loc + data_loc_len + 2
    close_paren_loc = python_call.find(')')

    data_loc = python_call[location_1 + 1: comma_loc - 1]
    target_loc = python_call[location_2 + 1: close_paren_loc - 1]

    # Read data from
    data = pd.read_csv(data_loc, index_col=0)
    target = pd.read_csv(target_loc, index_col=0)

    data_plus_target = pd.concat([data, target], axis=1)

    num_examples = data.shape[0]

    num_examples_01 = int(np.floor(num_examples * 0.01))
    num_examples_05 = int(np.floor(num_examples * 0.05))
    num_examples_10 = int(np.floor(num_examples * 0.10))

    data_plus_target_01 = data_plus_target.sample(num_examples_01)
    data_plus_target_05 = data_plus_target.sample(num_examples_05)
    data_plus_target_10 = data_plus_target.sample(num_examples_10)

    data_01 = data_plus_target_01.iloc[:, :data.shape[1]]
    data_05 = data_plus_target_05.iloc[:, :data.shape[1]]
    data_10 = data_plus_target_10.iloc[:, :data.shape[1]]

    target_01 = data_plus_target_01.iloc[:, data.shape[1]:]
    target_05 = data_plus_target_05.iloc[:, data.shape[1]:]
    target_10 = data_plus_target_10.iloc[:, data.shape[1]:]

    data_01.to_csv('mnist_data/data_01.csv')
    data_05.to_csv('mnist_data/data_05.csv')
    data_10.to_csv('mnist_data/data_10.csv')

    target_01.to_csv('mnist_data/target_01.csv')
    target_05.to_csv('mnist_data/target_05.csv')
    target_10.to_csv('mnist_data/target_10.csv')

    module = importlib.import_module(moduleName)

    string_01 = 'module.' + python_call.replace(data_loc, 'mnist_data/data_01.csv').replace(target_loc, 'mnist_data/target_01.csv')
    string_05 = 'module.' + python_call.replace(data_loc, 'mnist_data/data_05.csv').replace(target_loc, 'mnist_data/target_05.csv')
    string_10 = 'module.' + python_call.replace(data_loc, 'mnist_data/data_10.csv').replace(target_loc, 'mnist_data/target_10.csv')

    start = time.time()
    exec(string_01)
    finish = time.time()

    time_01 = finish - start

    start = time.time()
    exec(string_05)
    finish = time.time()

    time_05 = finish-start

    start = time.time()
    exec(string_10)
    finish = time.time()

    time_10 = finish-start

    return num_examples_01, time_01, num_examples_05, time_05, num_examples_10, time_10

if __name__ == '__main__':
    algo_runner("run_mnist(data_loc='mnist_data/mnist_data_20k.csv', target_loc='mnist_data/mnist_target_20k.csv')", 'keras_mnist_3')
