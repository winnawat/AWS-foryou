import boto3

import pandas as pd

ON_DEMAND_PRICING_CSV = 'https://tinyurl.com/yykw7p8c'
ON_DEMAND_PRICES = pd.read_csv(ON_DEMAND_PRICING_CSV,
                               error_bad_lines=False,
                               warn_bad_lines=False)


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


def get_instance_pricing(instance_type):
    """
    Get the spot and on demand price of an instance type
    in all the regions at current instant
    :param instance_type: EC2 instance type
    :return: a pandas DataFrame with columns as
             region, spot price and on demand price
    """
    all_regions = get_all_regions()

    spot_price_list = []
    on_demand_price_list = []

    for region_name in all_regions:
        spot_price = get_spot_price(instance_type, region_name)
        on_demand_price = get_on_demand_price(instance_type,
                                              region_name)

        spot_price_list.append(spot_price)
        on_demand_price_list.append(on_demand_price)

    return pd.DataFrame({'region': all_regions,
                         'spot_price': spot_price_list,
                         'on_demand_price': on_demand_price_list})
