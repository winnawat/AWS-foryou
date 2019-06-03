"""
Script that fetchs information realted to current AWS instance.
instance type and region.
returns dictionary
{
'instancetype': instancetype,
'region': region
}
"""


import requests


def get_instance():
    """
    Generate the EC2 instance type
    """
    req = requests.get("http://169.254.169.254/latest/dynamic/instance-identity/document")
    response_json = req.json()
    instancetype = response_json.get('instanceType')
    region = response_json.get('region')
    return {'instancetype': instancetype, 'region': region}
