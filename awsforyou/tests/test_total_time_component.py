"""this module contains three tests for the total time component"""
import unittest
import numpy as np
from awsforyou import total_time_component

TIMES_LIN = np.array([1, 5, 10])
TIMES_NLOGN = np.array([0, 8.04718956, 23.02585093])
TIMES_LOG = np.array([1, 8, 11])
TIMES_SQRD = np.array([1, 5, 10])

EXPT_TIME_LIN = 100
EXPT_TIME_NLOGN_RANGE = [459, 461]
EXPT_TIME_LOG_RANGE = [20, 22]
EXPT_TIME_SQRD = [10000]


class TestPermits(unittest.TestCase):
    """
    this class contains tests for log, squared, and linear times
    """

    def test_for_linear(self):
        """
        test for linear time
        """
        calc_linear = int(total_time_component.find_total_time(TIMES_LIN)[0])
        self.assertAlmostEqual(calc_linear, EXPT_TIME_LIN)

    def test_for_nlogn(self):
        """
        test for nlogn time
        """
        calc_nlogn = int(total_time_component.find_total_time(TIMES_NLOGN)[0])
        self.assertGreater(EXPT_TIME_NLOGN_RANGE[1], calc_nlogn)
        self.assertLess(EXPT_TIME_NLOGN_RANGE[0], calc_nlogn)

    def test_for_log(self):
        """
        test for log time
        """
        calc_log = int(total_time_component.find_total_time(TIMES_LOG)[0])
        self.assertGreater(EXPT_TIME_LOG_RANGE[1], calc_log)
        self.assertLess(EXPT_TIME_LOG_RANGE[0], calc_log)

    def test_for_squared(self):
        """
        test for squared time
        """
        calc_sqrd = int(total_time_component.find_total_time(TIMES_SQRD)[0])
        self.assertAlmostEqual(calc_sqrd, EXPT_TIME_LINEAR)
