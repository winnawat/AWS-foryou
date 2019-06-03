"""
Module that runs a simple perceptron on MNIST dataset.
"""


import sys
sys.path.append('..')
import unittest
import algo_runner
import keras_mnist
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.datasets import fetch_covtype


def test_find_data_target():
    TESTSTRING = "run_mnist(data_loc='mnist_data/mnist_data_20k.csv', " \
                  "target_loc='mnist_data/mnist_target_20k.csv')"
    data, target = algo_runner.find_data_target(TESTSTRING)
    assert data == "mnist_data/mnist_data_20k.csv", "data string not found case 1"
    assert target == "mnist_data/mnist_target_20k.csv", "target string not found case 1"

    TESTSTRING = "run_mnist(target_loc='mnist_data/mnist_target_20k.csv', " \
                 "data_loc='mnist_data/mnist_data_20k.csv')"
    data, target = algo_runner.find_data_target(TESTSTRING)
    assert data == "mnist_data/mnist_data_20k.csv", "data string not found case 2"
    assert target == "mnist_data/mnist_target_20k.csv", "target string not found case2"

    TESTSTRING = "run_mnist(data_loc = 'mnist_data/mnist_data_20k.csv', " \
                 "target_loc = 'mnist_data/mnist_target_20k.csv')"
    data, target = algo_runner.find_data_target(TESTSTRING)
    assert data == "mnist_data/mnist_data_20k.csv", "data string not found case 3"
    assert target == "mnist_data/mnist_target_20k.csv", "target string not found case 3"


    TESTSTRING = 'run_mnist(data_loc = "mnist_data/mnist_data_20k.csv", ' \
                 'target_loc = "mnist_data/mnist_target_20k.csv")'
    data, target = algo_runner.find_data_target(TESTSTRING)
    assert data == "mnist_data/mnist_data_20k.csv", "data string not found case 3"
    assert target == "mnist_data/mnist_target_20k.csv", "target string not found case 3"

    return None

def test_select_data():
    #case less than 10000 rows:
    iris = load_iris()
    x = iris['data']
    y = iris['target']
    x = pd.DataFrame(x)
    y = pd.DataFrame(y)
    pct_examples_1, pct_examples_2, pct_examples_3 = algo_runner.select_data(x, y)
    assert np.isclose(pct_examples_1, 0.1, rtol=0.001, atol=0.001), \
        "pct_examples_1 case lt 10000 not equal to 0.05"
    assert np.isclose(pct_examples_2, 0.2, rtol=0.001, atol=0.001), \
        "pct_examples_2 case lt 10000 not equal to 0.1"
    assert np.isclose(pct_examples_3, 0.3, rtol=0.001, atol=0.001), \
        "pct_examples_2 case lt 10000 not equal to 0.15"

    #case greater than 10000 less than 100000 rows:
    x_train, y_train, x_test, y_test = keras_mnist.KerasMnist().get_data()
    pct_examples_1, pct_examples_2, pct_examples_3 = algo_runner.select_data(x_train, y_train)
    assert np.isclose(pct_examples_1, 0.05, rtol = 0.001, atol = 0.001), \
        "pct_examples_1 case gt 10000 lt 100000 not equal to 0.05"
    assert np.isclose(pct_examples_2, 0.10, rtol = 0.001, atol = 0.001), \
        "pct_examples_2 case gt 10000 lt 100000 not equal to 0.1"
    assert np.isclose(pct_examples_3, 0.15, rtol = 0.001, atol = 0.001), \
        "pct_examples_2 case gt 10000 lt 100000 not equal to 0.15"

    #Case greater than 100000 rows:
    covtype = fetch_covtype()
    x = covtype['data']
    y = covtype['target']
    x = pd.DataFrame(x)
    y = pd.DataFrame(y)
    pct_examples_1, pct_examples_2, pct_examples_3 = algo_runner.select_data(x, y)
    assert np.isclose(pct_examples_1, 0.01, rtol=0.001, atol=0.001), \
        "pct_examples_1 case gt 100000 not equal to 0.01"
    assert np.isclose(pct_examples_2, 0.02, rtol=0.001, atol=0.001), \
        "pct_examples_2 case gt 100000 not equal to 0.02"
    assert np.isclose(pct_examples_3, 0.03, rtol=0.001, atol=0.001), \
        "pct_examples_2 case gt 100000 not equal to 0.03"
    return None

def test_algo_runner():
    dat = algo_runner.algo_runner("KerasMnist().run_mnist(data_loc='data/mnist_data/"
                                  "mnist_data_20k.csv', target_loc='data/mnist_data/"
                                  "mnist_target_20k.csv')", 'keras_mnist')
    for out in dat:
        assert type(out) == float, "algo_runner out dtype not float"

    return None


