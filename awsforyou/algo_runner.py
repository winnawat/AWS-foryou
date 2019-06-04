"""
Script that trains a simple perceptron using the keras library on the MNIST
dataset.  This script is used as a test for the AWS_foryou algo_runner
component.
"""

import importlib
import re
import time
import numpy as np
import pandas as pd


def find_data_target(python_call):
    """
    Finds the location of 'data_loc = ' and 'target_loc = ' in python_call.
    Helper function for algo_runner.

    :param python_call: string that calls a python function with data_loc and
    target_loc as parameters
    :return: data_len: int length of 'data_loc =' call
    :return: data_call: str location of data
    :return: target_len: int length of 'target_loc =' call
    :return: target_call: str location of target
    """

    data_len_span = re.search(r"data_loc[ ]*=[ ]*", python_call).span()
    # re search for comma or end paren [,|)]
    data_loc_span = re.search("^.*?(?=[,|)])",
                              python_call[data_len_span[1]:]).span()
    data_call = python_call[data_len_span[1]+1:
                            data_len_span[1] + data_loc_span[1]-1]

    target_len_span = re.search(r"target_loc[ ]*=[ ]*", python_call).span()
    # re search for comma or end paren [,|)]
    target_loc_span = re.search("^.*?(?=[,|)])",
                                python_call[target_len_span[1]:]).span()
    target_call = python_call[target_len_span[1]+1:
                              target_len_span[1] + target_loc_span[1]-1]

    return data_call, target_call


def select_data(data, target):
    """
    Splits data into three groups for timing purposes based on the size of the
    dataset.

    :param data: pandas.DataFrame data for algorithm
    :param target: pandas.DataFrame target for algorithm
    :return pct_examples_1: percent of examples in the first iteration
    :return pct_examples_2: percent of examples in the second iteration
    :return pct_examples_3: percent of examples in the third iteration
    """

    data_plus_target = pd.concat([data, target], axis=1)
    num_examples = data_plus_target.shape[0]

    if num_examples >= 100000:
        num_examples_1 = int(np.floor(num_examples * 0.01))
        num_examples_2 = int(np.floor(num_examples * 0.02))
        num_examples_3 = int(np.floor(num_examples * 0.03))

    elif num_examples >= 10000:
        num_examples_1 = int(np.floor(num_examples * 0.05))
        num_examples_2 = int(np.floor(num_examples * 0.10))
        num_examples_3 = int(np.floor(num_examples * 0.15))
    else:
        num_examples_1 = int(np.floor(num_examples * 0.1))
        num_examples_2 = int(np.floor(num_examples * 0.2))
        num_examples_3 = int(np.floor(num_examples * 0.3))

    pct_examples_1 = num_examples_1 / num_examples
    pct_examples_2 = num_examples_2 / num_examples
    pct_examples_3 = num_examples_3 / num_examples

    data_plus_target_1 = data_plus_target.sample(num_examples_1)
    data_plus_target_2 = data_plus_target.sample(num_examples_2)
    data_plus_target_3 = data_plus_target.sample(num_examples_3)

    data_1 = data_plus_target_1.iloc[:, :data.shape[1]]
    data_2 = data_plus_target_2.iloc[:, :data.shape[1]]
    data_3 = data_plus_target_3.iloc[:, :data.shape[1]]

    target_1 = data_plus_target_1.iloc[:, data.shape[1]:]
    target_2 = data_plus_target_2.iloc[:, data.shape[1]:]
    target_3 = data_plus_target_3.iloc[:, data.shape[1]:]

    data_1.to_csv('data/data_1.csv')
    data_2.to_csv('data/data_2.csv')
    data_3.to_csv('data/data_3.csv')

    target_1.to_csv('data/target_1.csv')
    target_2.to_csv('data/target_2.csv')
    target_3.to_csv('data/target_3.csv')

    return pct_examples_1, pct_examples_2, pct_examples_3


def time_algo(call_string, module_name):
    """
    Times the execution of a python call string.
    :param call_string: str string that calls a python module and executes an
    algorithm
    :param module_name: str name of module from which function is called
    :return run_time: float time in seconds required to execute python call
    string
    """

    module = importlib.import_module(module_name)

    start = time.time()
    exec(call_string)
    finish = time.time()
    run_time = finish - start

    return run_time


def algo_runner(python_call, module_name):
    """
    Calls an arbitrary module and runs the module with three different amounts
    of data for the purpose of timing the module and predicting how long the
    module will take to run with entire data set.

    :param python_call: str python string calling the algorithm to be timed
    :param module_name: name of module from which function is called
    :return times:
    :return percents:
    """

    data_call, target_call = find_data_target(python_call)

    data = pd.read_csv(data_call, index_col=0)
    target = pd.read_csv(target_call, index_col=0)

    pct_examples_1, pct_examples_2, pct_examples_3 = select_data(data, target)

    string_1 = 'module.' + python_call.replace(data_call, 'data/data_1.csv')\
        .replace(target_call, 'data/target_1.csv')
    string_2 = 'module.' + python_call.replace(data_call, 'data/data_2.csv')\
        .replace(target_call, 'data/target_2.csv')
    string_3 = 'module.' + python_call.replace(data_call, 'data/data_3.csv')\
        .replace(target_call, 'data/target_3.csv')

    time_1 = time_algo(string_1, module_name)
    time_2 = time_algo(string_2, module_name)
    time_3 = time_algo(string_3, module_name)

    times = [time_1, time_2, time_3]
    percents = [pct_examples_1, pct_examples_2, pct_examples_3]

    return times, percents
