"""
Module that runs a simple perceptron on MNIST dataset.
"""

import unittest
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.datasets import fetch_covtype
from awsforyou import algo_runner


class TestAlgoRunner(unittest.TestCase):

    def test_find_data_target(self):
        """
        Tests the find_data_target function in algo_runner.py
        :return: None
        """

        test_str = "run_mnist(data_loc='mnist_data/mnist_data_20k.csv', " \
                   "target_loc='mnist_data/mnist_target_20k.csv')"
        data, target = algo_runner.find_data_target(test_str)
        self.assertTrue(data == "mnist_data/mnist_data_20k.csv")
        self.assertTrue(target == "mnist_data/mnist_target_20k.csv")

        test_str = "run_mnist(target_loc='mnist_data/mnist_target_20k.csv'," \
                   "data_loc='mnist_data/mnist_data_20k.csv')"
        data, target = algo_runner.find_data_target(test_str)
        self.assertTrue(data == "mnist_data/mnist_data_20k.csv")
        self.assertTrue(target == "mnist_data/mnist_target_20k.csv")

        test_str = "run_mnist(data_loc = 'mnist_data/mnist_data_20k.csv', " \
                   "target_loc = 'mnist_data/mnist_target_20k.csv')"
        data, target = algo_runner.find_data_target(test_str)
        self.assertTrue(data == "mnist_data/mnist_data_20k.csv")
        self.assertTrue(target == "mnist_data/mnist_target_20k.csv")

        test_str = 'run_mnist(data_loc = "mnist_data/mnist_data_20k.csv", ' \
                   'target_loc = "mnist_data/mnist_target_20k.csv")'
        data, target = algo_runner.find_data_target(test_str)
        self.assertTrue(data == "mnist_data/mnist_data_20k.csv")
        self.assertTrue(target == "mnist_data/mnist_target_20k.csv")

        return None

    def test_select_data(self):
        """
        Tests the select_data function in algo_runner.py
        :return: None
        """

        # case less than 10000 rows:
        iris = load_iris()
        data = iris['data']
        target = iris['target']
        data = pd.DataFrame(data)
        target = pd.DataFrame(target)
        pct_examples_1, pct_examples_2, pct_examples_3 = \
            algo_runner.select_data(data, target)
        self.assertTrue(np.isclose(pct_examples_1, 0.1, rtol=0.001,
                                   atol=0.001))
        self.assertTrue(np.isclose(pct_examples_2, 0.2, rtol=0.001,
                                   atol=0.001))
        self.assertTrue(np.isclose(pct_examples_3, 0.3, rtol=0.001,
                                   atol=0.001))

        # case greater than 10000 less than 100000 rows:
        x_train = pd.read_csv('data/mnist_data/mnist_data_20k.csv')
        y_train = pd.read_csv('data/mnist_data/mnist_target_20k.csv')
        pct_examples_1, pct_examples_2, pct_examples_3 = \
            algo_runner.select_data(x_train, y_train)
        self.assertTrue(np.isclose(pct_examples_1, 0.05, rtol=0.001,
                                   atol=0.001))
        self.assertTrue(np.isclose(pct_examples_2, 0.10, rtol=0.001,
                                   atol=0.001))
        self.assertTrue(np.isclose(pct_examples_3, 0.15, rtol=0.001,
                                   atol=0.001))

        # Case greater than 100000 rows:
        covtype = fetch_covtype()
        data = covtype['data']
        target = covtype['target']
        data = pd.DataFrame(data)
        target = pd.DataFrame(target)
        pct_examples_1, pct_examples_2, pct_examples_3 = \
            algo_runner.select_data(data, target)
        self.assertTrue(np.isclose(pct_examples_1, 0.01, rtol=0.001,
                                   atol=0.001))
        self.assertTrue(np.isclose(pct_examples_2, 0.02, rtol=0.001,
                                   atol=0.001))
        self.assertTrue(np.isclose(pct_examples_3, 0.03, rtol=0.001,
                                   atol=0.001))
        return None

    def test_algo_runner(self):
        """
        tests the algo_runner functino in algo_runner.py
        :return: None
        """

        run_string = "run_mnist(data_loc='data/mnist_data/" \
                     "mnist_data_20k.csv', target_loc='data/mnist_data/" \
                     "mnist_target_20k.csv')"
        times, percents = algo_runner.algo_runner(run_string, 'keras_mnist')

        self.assertTrue(isinstance(times, list))
        for item in times:
            self.assertTrue(isinstance(item, float))

        self.assertTrue(isinstance(percents, list))
        for item in percents:
            self.assertTrue(isinstance(item, float))

        return None
