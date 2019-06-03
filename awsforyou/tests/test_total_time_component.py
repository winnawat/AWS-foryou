"""this module contains three tests for the total time component"""
import unittest
from awsforyou import total_time_component
import numpy as np

times_linear = np.array([1, 5, 10])
times_sqrd = np.array([1, 25, 100])
times_log = np.array([1, 8, 11])

expected_time_linear = 100
expected_time_sqrd = 10000
expt_time_log_range = [20, 22]


class TestPermits(unittest.TestCase):
    """
    this class contains tests for log, squared, and linear times
    """

    def test_for_linear(self):
        """
        test for linear time
        """
        calc_linear = int(total_time_component.find_total_time(times_linear))
        TorF = calc_linear == expected_time_linear
        assert TorF

    def test_for_squared(self):
        """
        test for n^2 time
        """
        calc_sqrd = int(total_time_component.find_total_time(times_sqrd))
        TorF = calc_sqrd == expected_time_sqrd
        assert TorF

    def test_for_log(self):
        """
        test for log time
        """
        calc_log = int(total_time_component.find_total_time(times_log))
        assert expt_time_log_range[1] > calc_log > expt_time_log_range[0]


SUITE = unittest.TestLoader().loadTestsFromTestCase(TestPermits)
_ = unittest.TextTestRunner().run(SUITE)
