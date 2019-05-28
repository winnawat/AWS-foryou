import requests


def get_instance():
    """
    Generate the EC2 instance type
    """
    r = requests.get("http://169.254.169.254"
                     + "/latest/dynamic/instance-identity/document")
    response_json = r.json()
    instancetype = response_json.get('instanceType')
    region = response_json.get('region')
    return {'instancetype': instancetype, 'region': region, }
