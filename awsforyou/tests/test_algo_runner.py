"""
Module that runs a simple perceptron on MNIST dataset.
"""

import os
import shutil
import unittest
import numpy as np
import pandas as pd
from keras.utils import np_utils
from keras.datasets import mnist
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

        self.assertEqual(data, "mnist_data/mnist_data_20k.csv")
        self.assertEqual(target, "mnist_data/mnist_target_20k.csv")

        test_str = "run_mnist(target_loc='mnist_data/mnist_target_20k.csv'," \
                   "data_loc='mnist_data/mnist_data_20k.csv')"
        data, target = algo_runner.find_data_target(test_str)
        self.assertEqual(data, "mnist_data/mnist_data_20k.csv")
        self.assertEqual(target, "mnist_data/mnist_target_20k.csv")

        test_str = "run_mnist(data_loc = 'mnist_data/mnist_data_20k.csv', " \
                   "target_loc = 'mnist_data/mnist_target_20k.csv')"
        data, target = algo_runner.find_data_target(test_str)
        self.assertEqual(data, "mnist_data/mnist_data_20k.csv")
        self.assertEqual(target, "mnist_data/mnist_target_20k.csv")

        test_str = 'run_mnist(data_loc = "mnist_data/mnist_data_20k.csv", ' \
                   'target_loc = "mnist_data/mnist_target_20k.csv")'
        data, target = algo_runner.find_data_target(test_str)
        self.assertEqual(data, "mnist_data/mnist_data_20k.csv")
        self.assertEqual(target, "mnist_data/mnist_target_20k.csv")

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
        self.assertTrue(np.isclose(pct_examples_1, 0.05, rtol=0.01,
                                   atol=0.01))
        self.assertTrue(np.isclose(pct_examples_2, 0.10, rtol=0.01,
                                   atol=0.01))
        self.assertTrue(np.isclose(pct_examples_3, 0.15, rtol=0.01,
                                   atol=0.01))

        # case greater than 10000 less than 100000 rows:
        (x_train, y_train), (x_test, y_test) = mnist.load_data()
        num_pixels = x_train.shape[1] * x_train.shape[2]
        x_train = x_train.reshape(x_train.shape[0], num_pixels).astype(
            'float32')
        x_train = x_train / 255
        y_train = np_utils.to_categorical(y_train)

        x_train = pd.DataFrame(x_train)
        y_train = pd.DataFrame(y_train)

        pct_examples_1, pct_examples_2, pct_examples_3 = \
            algo_runner.select_data(x_train, y_train)
        self.assertTrue(np.isclose(pct_examples_1, 0.02, rtol=0.001,
                                   atol=0.001))
        self.assertTrue(np.isclose(pct_examples_2, 0.04, rtol=0.001,
                                   atol=0.001))
        self.assertTrue(np.isclose(pct_examples_3, 0.06, rtol=0.001,
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

    def test_run_algo(self):
        """
        tests the algo_runner functino in algo_runner.py
        :return: None
        """

        print('Loading mnist dataset...')
        (X_train, y_train), (X_test, y_test) = mnist.load_data()
        print('Finished loading mnist dataset.')

        # flatten 28*28 images to a 784 vector for each image
        num_pixels = X_train.shape[1] * X_train.shape[2]
        X_train = X_train.reshape(X_train.shape[0], num_pixels).astype(
            'float32')
        X_test = X_test.reshape(X_test.shape[0], num_pixels).astype('float32')

        data = pd.concat([pd.DataFrame(X_train), pd.DataFrame(X_test)], axis=0)

        # y_train = np_utils.to_categorical(y_train)
        # y_test = np_utils.to_categorical(y_test)

        target = pd.concat([pd.DataFrame(y_train), pd.DataFrame(y_test)],
                           axis=0)

        this_dir = os.path.dirname(os.path.abspath(__file__))

        if not os.path.exists(this_dir + '/data'):
            os.mkdir(this_dir + '/data')

        data_path = os.path.join(this_dir, "data/mnist_data.csv")
        target_path = os.path.join(this_dir, "data/mnist_target.csv")

        # Data and target to csv
        print('Saving data to disk.')
        data.to_csv(data_path)
        target.to_csv(target_path)
        print('Finished saving data to disk.')

        run_string = "run_mnist(data_loc='" + data_path + "', target_loc='" \
                     + target_path + "')"

        times, percents = algo_runner.run_algo(run_string,
                                               'awsforyou.tests.'
                                               'test_keras_mnist')

        self.assertTrue(isinstance(times, list))
        for item in times:
            self.assertTrue(isinstance(item, float))

        self.assertTrue(isinstance(percents, list))
        for item in percents:
            self.assertTrue(isinstance(item, float))

        return None
