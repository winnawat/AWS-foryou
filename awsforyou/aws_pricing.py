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


def get_spot_price(instance_type, region_name):
    """
    Get spot price at current instant of an instance in a
    given region
    :param instance_type: EC2 instance type
    :param region_name: AWS regions name
    :return: a floating point number - spot price
    """
    ec2_client = boto3.client('ec2', region_name=region_name)
    response = ec2_client.describe_spot_price_history(
        InstanceTypes=[instance_type],
        ProductDescriptions=['Linux/UNIX'],
        MaxResults=1)

    spot_price = response['SpotPriceHistory'][0]['SpotPrice']
    return float(spot_price)


def get_on_demand_price(instance_type, region_name):
    """
    Get on demand price at current instant of an instance in a
    given region
    :param instance_type: EC2 instance type
    :param region_name: AWS regions name
    :return: a floating point number - on demand price
    """
    price = ON_DEMAND_PRICES.loc[
        (ON_DEMAND_PRICES['instanceType'] == instance_type) &
        (ON_DEMAND_PRICES['region'] == region_name) &
        (ON_DEMAND_PRICES['operatingSystem'] == 'Linux')]['price']
    return price.item()


def get_instance_pricing(instance_types):
    """
    Get the spot and on demand price of an instance type
    in all the regions at current instant
    :param instance_types: EC2 instance type
    :return: a pandas DataFrame with columns as
             region, spot price and on demand price
    """
    all_regions = get_all_regions()

    instance_type_list = []
    regions_list = []
    spot_price_list = []
    on_demand_price_list = []

    for instance_type in instance_types:
        for region_name in all_regions:
            try:
                spot_price = get_spot_price(instance_type, region_name)
                on_demand_price = get_on_demand_price(instance_type,
                                                      region_name)
                instance_type_list.append(instance_type)
                regions_list.append(region_name)
                spot_price_list.append(spot_price)
                on_demand_price_list.append(on_demand_price)
            except (IndexError, KeyError):
                LOGGER.warning('Failed to fetch Price for instance {} in '
                               'region {}'.format(instance_type, region_name))

        print(len(instance_type_list))
        print(len(all_regions))
        print(len(instance_type_list))

    return pd.DataFrame({DF_COL_INSTANCE_TYPE: instance_type_list,
                         DF_COL_REGION: regions_list,
                         DF_COL_SPOT_PRICE: spot_price_list,
                         DF_COL_ON_DEMAND_PRICE: on_demand_price_list})
