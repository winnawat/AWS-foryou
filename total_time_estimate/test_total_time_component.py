"""this module contains three tests for the total time component"""
import unittest
import numpy as np
import pandas as pd

times_linear = np.array([1, 5, 10])
times_sqrd = np.array([1, 25, 100])
times_log = np.array([1, 8, 11])

expected_time_linear = 100
expected_time_sqrd = 100
expected_time_log_range = [22, 23]


class TestPermits(unittest.TestCase):
    """
    this class contains tests for log, squared, and linear times
    """

    def test_for_linear(self):
        """
        test for linear time
        """
        linear = find_total_time(times_linear) == expected_time_linear
        assert linear

    def test_for_squared(self):
        """
        test for n^2 time
        """
        squared = find_total_time(times_sqrd) == expected_time_sqrd
        assert squared

    def test_for_log(self):
        """
        test for log time
        """
        calc_time_log = find_total_time(times_log)
        logarithmic = calc_time_log < expected_time_log_range[1] and calc_time_log > expected_time_log_range[0]
        assert logarithmic


SUITE = unittest.TestLoader().loadTestsFromTestCase(TestPermits)
_ = unittest.TextTestRunner().run(SUITE)
