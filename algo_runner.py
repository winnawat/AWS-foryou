"""
Script that trains a simple perceptron using the keras library on the MNIST
dataset.  This script is used as a test for the AWS_foryou algo_runner component.
"""

import importlib
import numpy as np
import os
import pandas as pd
import re
import sys
import time

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

def find_data_target(python_call):
    """
    Finds the location of 'data_loc = ' and 'target_loc = ' in python_call.  Helper function for algo_runner.

    :param python_call: string that calls a python function with data_loc and target_loc as parameters
    :return: data_len: int length of 'data_loc =' call
    :return: data_call: str location of data
    :return: target_len: int length of 'target_loc =' call
    :return: target_call: str location of target
    """

    data_len_span = re.search(r"data_loc[ ]*=[ ]*", python_call).span()
    data_len = data_len_span[1] - data_len_span[0]
    data_loc_span = re.search("^.*?(?=[,|)])", python_call[data_len_span[1]:]).span()
    data_call = python_call[data_len_span[1]+1:data_len_span[1] + data_loc_span[1]-1]

    target_len_span = re.search(r"target_loc[ ]*=[ ]*", python_call).span()
    target_len = target_len_span[1] - target_len_span[0]
    target_loc_span = re.search("^.*?(?=[,|)])", python_call[target_len_span[1]:]).span()
    target_call = python_call[target_len_span[1]+1:target_len_span[1] + target_loc_span[1]-1]

    return data_len, data_call, target_len, target_call


def algo_runner(python_call, module_name):
    """
    Calls an arbitrary module and runs the module with three different amounts of data for the purpose of
    timing the module and predicting how long the module will take to run with entire data set.

    :param python_call: str python string calling the algorithm to be timed
    :param module_name: str name of module
    :return pct_examples_01: float fraction of examples tested in first iteration
    :return time_01: float: time in seconds required to run algorithm with pct_examples_01
    :return pct_examples_05: float fraction of examples tested in second iteration
    :return time_05: float time in seconds required to run algorithm with pct_examples_05
    :return pct_examples_10: float fraction of examples tested in third iteration
    :return time_10: float time in seconds required to run algorithm with pct_examples_10
    """

    data_len, data_call, target_len, target_call = find_data_target(python_call)

    # Read data from
    data = pd.read_csv(data_call, index_col=0)
    target = pd.read_csv(target_call, index_col=0)

    data_plus_target = pd.concat([data, target], axis=1)

    num_examples = data.shape[0]

    num_examples_01 = int(np.floor(num_examples * 0.01))
    num_examples_05 = int(np.floor(num_examples * 0.05))
    num_examples_10 = int(np.floor(num_examples * 0.10))

    pct_examples_01 = num_examples_01 / num_examples
    pct_examples_05 = num_examples_05 / num_examples
    pct_examples_10 = num_examples_10 / num_examples

    data_plus_target_01 = data_plus_target.sample(num_examples_01)
    data_plus_target_05 = data_plus_target.sample(num_examples_05)
    data_plus_target_10 = data_plus_target.sample(num_examples_10)

    data_01 = data_plus_target_01.iloc[:, :data.shape[1]]
    data_05 = data_plus_target_05.iloc[:, :data.shape[1]]
    data_10 = data_plus_target_10.iloc[:, :data.shape[1]]

    target_01 = data_plus_target_01.iloc[:, data.shape[1]:]
    target_05 = data_plus_target_05.iloc[:, data.shape[1]:]
    target_10 = data_plus_target_10.iloc[:, data.shape[1]:]

    data_01.to_csv('data/data_01.csv')
    data_05.to_csv('data/data_05.csv')
    data_10.to_csv('data/data_10.csv')

    target_01.to_csv('data/target_01.csv')
    target_05.to_csv('data/target_05.csv')
    target_10.to_csv('data/target_10.csv')

    module = importlib.import_module(module_name)

    string_01 = 'module.' + python_call.replace(data_call, 'data/data_01.csv')\
        .replace(target_call, 'data/target_01.csv')
    string_05 = 'module.' + python_call.replace(data_call, 'data/data_05.csv')\
        .replace(target_call, 'data/target_05.csv')
    string_10 = 'module.' + python_call.replace(data_call, 'data/data_10.csv')\
        .replace(target_call, 'data/target_10.csv')

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

    return pct_examples_01, time_01, pct_examples_05, time_05, pct_examples_10, time_10


if __name__ == '__main__':
    algo_runner("run_mnist(data_loc='mnist_data/mnist_data_20k.csv', target_loc='mnist_data/mnist_target_20k.csv')",
                'keras_mnist_3')
