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
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


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


def select_data(data, target, num_pts):
    """
    Splits data into three groups for estimation of time taken to run whole
    100% of data set and order estimation.

    :param data: pandas.DataFrame data for algorithm
    :param target: pandas.DataFrame target for algorithm
    :param num_pts: number of independent points to be used for estimation
    :return pct_examples_1: percent of examples in the first iteration
    :return pct_examples_2: percent of examples in the second iteration
    :return pct_examples_3: percent of examples in the third iteration
    """

    data_plus_target = pd.concat([data, target], axis=1)
    num_examples = data_plus_target.shape[0]

    pct_examples_list = list(np.multiply(0.01, range(1, num_pts+1)))

    num_examples_list = []
    for pct_examples in pct_examples_list:
        num_examples_list.append(int(np.ceil(pct_examples * num_examples)))

    data_plus_target.head(1).iloc[:, :data.shape[1]].to_csv('data/data_0.csv')
    data_plus_target.head(1).iloc[:, data.shape[1]:].to_csv(
        'data/target_0.csv')

    iter_ = 1
    for num_examp in num_examples_list:
        data_plus_target_1 = data_plus_target.sample(num_examp)
        data_plus_target_1.iloc[:, :data.shape[1]].to_csv('data/data_' +
                                                          str(iter_) + '.csv')
        data_plus_target_1.iloc[:, data.shape[1]:].to_csv('data/target_' +
                                                          str(iter_) + '.csv')
        iter_ += 1

    return pct_examples_list


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


def algo_runner(python_call, module_name, num_pts=3, num_iter=3):
    """
    Calls an arbitrary module and runs the module with three different amounts
    of data for the purpose of timing the module and predicting how long the
    module will take to run with entire data set.

    :param python_call: str python string calling the algorithm to be timed
    :param module_name: str name of module from which function is called
    :param num_pts: int number of points for algo_runner to run against
    :param num_iter: int number of iterations for algo_runner to run
    :return times: list of times taken to run model in seconds
    :return percents: list of percentages of data run through model
    """

    data_call, target_call = find_data_target(python_call)

    data = pd.read_csv(data_call, index_col=0)
    target = pd.read_csv(target_call, index_col=0)

    pct_examples_list = select_data(data, target, num_pts)
    percents = []
    times = []
    for point in range(1, num_pts+1):
        for iter_ in range(num_iter):
            # string_1 = 'module.'
            p_call = python_call.replace(data_call, 'data/data_' +
                                         str(point) + '.csv')
            p_call = p_call.replace(target_call, 'data/target_' +
                                    str(point) + '.csv')
            string_1 = 'module.' + p_call
            times.append(time_algo(string_1, module_name))
            percents.append(pct_examples_list[point-1])
    percents = list(np.multiply(100, percents))
    return times, percents
