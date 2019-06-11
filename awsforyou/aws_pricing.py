import logging

import boto3

import pandas as pd

ON_DEMAND_PRICING_CSV = 'https://tinyurl.com/yykw7p8c'
ON_DEMAND_PRICES = pd.read_csv(ON_DEMAND_PRICING_CSV,
                               error_bad_lines=False,
                               warn_bad_lines=False)

DF_COL_INSTANCE_TYPE = 'instance_type'
DF_COL_REGION = 'region'
DF_COL_SPOT_PRICE = 'spot_price'
DF_COL_ON_DEMAND_PRICE = 'on_demand_price'


LOGGER = logging.getLogger(__name__)


def get_all_regions():
    """
    Get all regions served by AWS
    :return: a list of string
    """
    ec2 = boto3.client('ec2', 'us-east-1')
    response = ec2.describe_regions()
    return [region['RegionName'] for region in response['Regions']]


def get_spot_price(instance_types, region_name):
    """
    Get spot price at current instant of an instance in a
    given region
    :param instance_types: EC2 instance type
    :param region_name: AWS regions name
    :return: a dictionary with instance type as key and  spot price as value
    """
    ec2_client = boto3.client('ec2', region_name=region_name)
    response = ec2_client.describe_spot_price_history(
        InstanceTypes=instance_types,
        ProductDescriptions=['Linux/UNIX'],
        MaxResults=len(instance_types) * 6)

    spot_prices = {}

    spot_price_list = response['SpotPriceHistory']
    for sp in spot_price_list:
        if sp['InstanceType'] not in spot_prices:
            spot_prices[sp['InstanceType']] = float(sp['SpotPrice'])

    instance_type_list = []
    spot_price_list = []
    for instance_type, spot_price in spot_prices.items():
        instance_type_list.append(instance_type)
        spot_price_list.append(spot_price)

    return pd.DataFrame({DF_COL_INSTANCE_TYPE: instance_type_list,
                         DF_COL_SPOT_PRICE: spot_price_list})


def get_on_demand_price(instance_types, region_name):
    """
    Get on demand price at current instant of an instance in a
    given region
    :param instance_types: EC2 instance types
    :param region_name: AWS regions name
    :return: a dictionary as instance type as key and
    """
    instance_prices = ON_DEMAND_PRICES.loc[
        (ON_DEMAND_PRICES['instanceType'].isin(instance_types)) &
        (ON_DEMAND_PRICES['region'] == region_name) &
        (ON_DEMAND_PRICES['operatingSystem'] == 'Linux')]

    instance_type_list = instance_prices['instanceType']
    on_demand_price_list = instance_prices['price']

    return pd.DataFrame({DF_COL_INSTANCE_TYPE: instance_type_list,
                         DF_COL_ON_DEMAND_PRICE: on_demand_price_list})


def get_instance_pricing(instance_types):
    """
    Get the spot and on demand price of an instance type
    in all the regions at current instant
    :param instance_types: EC2 instance type
    :return: a pandas DataFrame with columns as
             region, spot price and on demand price
    """
    all_regions = get_all_regions()

    price_df = pd.DataFrame({DF_COL_INSTANCE_TYPE: [],
                             DF_COL_REGION: [],
                             DF_COL_SPOT_PRICE: [],
                             DF_COL_ON_DEMAND_PRICE: []})

    for region_name in all_regions:
        spot_prices = get_spot_price(instance_types, region_name)
        on_demand_prices = get_on_demand_price(instance_types, region_name)
        both_prices = pd.merge(spot_prices, on_demand_prices,
                               on=DF_COL_INSTANCE_TYPE)

        n_rows = both_prices.shape[0]
        region_list = n_rows * [region_name]
        both_prices[DF_COL_REGION] = region_list
        both_prices = both_prices[[DF_COL_INSTANCE_TYPE, DF_COL_REGION,
                                   DF_COL_SPOT_PRICE,
                                   DF_COL_ON_DEMAND_PRICE]]

        price_df = price_df.append(both_prices)

    return price_df
