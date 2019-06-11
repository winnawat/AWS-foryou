"""This module contains tests for the recommender module"""
import unittest
import pandas as pd
from awsforyou import recommender as rc
from awsforyou import benchmark_runner as br
from awsforyou import total_time_component as tt
from awsforyou import aws_pricing as ap


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

    def test_add_estimated_price(self):
        """
        This function tests adding the spot and on-demand pricing
        to the dataframe
        """
        benchmark_df = rc.get_benchmark_data()
        times, percents = [2, 4, 6], [1, 5, 10]
        est_time_user = tt.find_total_time(times, percents)
        user_benchmark = br.run_benchmark()
        est_time_aws = benchmark_df[['runtime']] \
            / user_benchmark * est_time_user[0]
        benchmark_df["estimated_time_aws"] = est_time_aws
        instance_types = benchmark_df["instance_type"].tolist()
        price = ap.get_instance_pricing(instance_types)
        complete_df = pd.merge(benchmark_df, price, on="instance_type")
        complete_df["est_cost_spot_price"] = \
            complete_df["estimated_time_aws"] \
            * complete_df["spot_price"] / 3600
        complete_df["est_cost_on_demand_price"] = \
            complete_df["estimated_time_aws"] \
            * complete_df["on_demand_price"] / 3600
        self.assertGreater(complete_df.shape[0], 0)
