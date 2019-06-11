"""This module contains tests for the recommender module"""
import unittest
from awsforyou import recommender as rc


class TestRecommender(unittest.TestCase):
    """
    this class contains tests
    """

    def test_for_benchmark_df_empty(self):
        """
        test to see if benchmark dataframe is empty
        """
        benchmark_df = rc.get_benchmark_data()
        self.assertGreater(benchmark_df.shape[0], 0)
