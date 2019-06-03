"""this module contains three tests for the total time component"""
import unittest
import numpy as np
from awsforyou import total_time_component

TIMES_LINEAR = np.array([1, 5, 10])
TIMES_SQRD = np.array([1, 25, 100])
TIMES_LOG = np.array([1, 8, 11])

EXPT_TIME_LINEAR = 100
EXPT_TIME_SQRD = 10000
EXPT_TIME_LOG_RANGE = [20, 22]


class TestPermits(unittest.TestCase):
    """
    this class contains tests for log, squared, and linear times
    """

    def test_for_linear(self):
        """
        test for linear time
        """
        calc_linear = int(total_time_component.find_total_time(TIMES_LINEAR))
        self.assertEqual(calc_linear, EXPT_TIME_LINEAR)

    def test_for_squared(self):
        """
        test for n^2 time
        """
        calc_sqrd = int(total_time_component.find_total_time(TIMES_SQRD))
        self.assertEqual(calc_sqrd, EXPT_TIME_SQRD)

    def test_for_log(self):
        """
        test for log time
        """
        calc_log = int(total_time_component.find_total_time(TIMES_LOG))
        self.assertGreater(EXPT_TIME_LOG_RANGE[1], calc_log)
        self.assertLess(EXPT_TIME_LOG_RANGE[0], calc_log)
