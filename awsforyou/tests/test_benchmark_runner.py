import os
import unittest

import pandas as pd

import benchmark_runner as bench


class TestGetData(unittest.TestCase):
    """
    Test cases for the function get_data
    """
    def test_get_data(self):
        """
        Testing the get data funciton
        """
        data = bench.get_data()
        x_train, y_train, x_test, y_test = data
        self.assertEqual((60000, 784), x_train.shape)
        self.assertEqual((60000, 10), y_train.shape)
        self.assertEqual((10000, 784), x_test.shape)
        self.assertEqual((10000, 10), y_test.shape)


class TestRunBenchmark(unittest.TestCase):
    """
    Test cases for the function run_benchmark
    """
    def test_runtime(self):
        """
        Check if output is indeed number of seconds
        """
        runtime = bench.run_benchmark(aws=False)
        self.assertIsInstance(runtime, float)
