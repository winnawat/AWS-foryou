"""
This module creates a dataframe with time and price estimates, this is used by
the GUI to recommend the least expensive or fastest options
"""
from awsforyou import algo_runner as ar
from awsforyou import benchmark_runner as br
from awsforyou import total_time_component as tt
from awsforyou import aws_pricing as ap
import pandas as pd

SECSINHR = 3600


def get_benchmark_data():
    """
    This function retrieves a csv file from our github, filters to columns
    instanceType and runtime, then reduces the rows to median runtime values
    and then returns this new dataframe
    """
    benchmark = pd.read_csv("https://raw.githubusercontent.com/winnawat/"
                            "AWS-foryou/master/data/aws-scorecard.csv",
                            index_col=False)
    benchmark = benchmark[benchmark.instancetype != 'local-machine']
    benchmark = benchmark[["instancetype", "runtime"]]
    benchmark.columns = ['instance_type', 'runtime']
    benchmark = benchmark.groupby(["instance_type"], as_index=False).median()
    return benchmark


def add_estimated_time_aws(dataframe, python_call, module_name):
    """
    This function estimates the time required to run the users algorithim on
    each instance and adds it to the dataframe
    :param python_call: str python string calling the algorithm to be timed
    :param module_name: str name of module from which function is called
    :param dataframe: the benchmark dataframe output from get_benchmark_data()
    :return: dataframe with added estimated times
    """
    times, percents = ar.run_algo(python_call, module_name)
    est_time_user = tt.find_total_time(times, percents)
    user_benchmark = br.run_benchmark()
    est_time_aws = dataframe[['runtime']]/user_benchmark * est_time_user[0]
    dataframe["estimated_time_aws"] = est_time_aws
    return dataframe


def add_estimated_price(df):
    """
    This function adds the spot and on-demand pricing to the dataframe
    """
    instance_types = df["instance_type"].tolist()
    price = ap.get_instance_pricing(instance_types)
    complete_df = pd.merge(df, price, on="instance_type")
    complete_df["est_cost_spot_price"] = \
        complete_df["estimated_time_aws"]*complete_df["spot_price"]/SECSINHR
    complete_df["est_cost_on_demand_price"] = \
        complete_df["estimated_time_aws"] \
        * complete_df["on_demand_price"]/SECSINHR
    return complete_df


def create_dataframe(python_call, module_name):
    """
    This function creates the completed dataframe by calling the functions:
    get_benchmark_data, add_estimated_time_aws, and add_estimated_price.
    """
    benchmark_df = get_benchmark_data()
    bench_time_df = add_estimated_time_aws(benchmark_df,
                                           python_call, module_name)
    complete_df = add_estimated_price(bench_time_df)
    return complete_df
