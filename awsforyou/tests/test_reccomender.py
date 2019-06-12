"""This module contains tests for the recommender module"""
import unittest

import pandas as pd

from awsforyou import algo_runner as ar
from awsforyou import benchmark_runner as br
from awsforyou import recommender as rc
from awsforyou import total_time_component as tt


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

    def test_for_time_df_empty(self):
        """
        test to see if added times dataframe is empty
        """
        benchmark_df = rc.get_benchmark_data()
        times, percents = [2, 4, 6], [1, 5, 10]
        est_time_user = tt.find_total_time(times, percents)
        user_benchmark = br.run_benchmark()
        est_time_aws = benchmark_df[['runtime']] / \
            user_benchmark * est_time_user[0]
        benchmark_df["estimated_time_aws"] = est_time_aws
        self.assertGreater(benchmark_df.shape[0], 0)

    def test_for_complete_df_empty(self):
        """
        test to see if added times dataframe is empty
        """
        benchmark_df = rc.get_benchmark_data()
        times, percents = [2, 4, 6], [1, 5, 10]
        est_time_user = tt.find_total_time(times, percents)
        user_benchmark = br.run_benchmark()
        est_time_aws = benchmark_df[['runtime']] \
            / user_benchmark * est_time_user[0]
        benchmark_df["estimated_time_aws"] = est_time_aws
        self.assertGreater(benchmark_df.shape[0], 0)

    def test_add_estimated_time_aws(self):
        ar.run_algo = mock_run_algo
        instance_type_list = ['t3.large', 'c5.xlarge', 't3.medium']
        runtime_list = [0.01, 0.02, 0.03]
        data_frame = pd.DataFrame({'instance_type': instance_type_list,
                                   'runtime': runtime_list})
        updated_df = rc.add_estimated_time_aws(data_frame, '', '')
        self.assertIsNotNone(updated_df)

    def test_add_estimated_price(self):
        ar.run_algo = mock_run_algo
        instance_type_list = ['t3.large', 'c5.xlarge', 't3.medium']
        runtime_list = [0.01, 0.02, 0.03]
        data_frame = pd.DataFrame({'instance_type': instance_type_list,
                                   'runtime': runtime_list})
        updated_df = rc.add_estimated_time_aws(data_frame, '', '')
        complete_df = rc.add_estimated_price(updated_df)
        self.assertIsNotNone(complete_df)

    def test_create_dataframe(self):
        ar.run_algo = mock_run_algo
        created_df = rc.create_dataframe('', '')
        self.assertIsNotNone(created_df)


def mock_run_algo(python_call, module_name):
    return [2, 4, 6], [1, 5, 10]
