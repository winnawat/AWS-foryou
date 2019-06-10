import unittest

import pandas as pd

from awsforyou import aws_pricing


class TestAwsPricing(unittest.TestCase):

    def test_get_all_regions(self):
        regions = aws_pricing.get_all_regions()
        self.assertIsNotNone(regions)
        self.assertGreater(len(regions), 0)

    def test_get_spot_pricing(self):
        price = aws_pricing.get_spot_price('t3.large', 'us-east-1')
        self.assertIsNotNone(price)

    def test_get_on_demand_pricing(self):
        price = aws_pricing.get_on_demand_price('t3.large', 'us-east-1')
        self.assertEquals(price, 0.0832)

    def test_get_all_pricing_one_instance(self):
        price_df = aws_pricing.get_instance_pricing(['t3.large'])
        self.assertIsInstance(price_df, pd.DataFrame)
        columns = list(price_df.columns)
        expected_columns = ['instance_type', 'region',
                            'spot_price', 'on_demand_price']
        self.assertEquals(columns, expected_columns)

    def test_get_all_pricing_multiple_instance(self):
        instance_type_list = ['c5.18xlarge', 'm5a.large', 'c5.xlarge']
        price_df = aws_pricing.get_instance_pricing(instance_type_list)
        self.assertIsInstance(price_df, pd.DataFrame)
        columns = list(price_df.columns)
        expected_columns = ['instance_type', 'region',
                            'spot_price', 'on_demand_price']
        instance_types_df = price_df[aws_pricing.DF_COL_INSTANCE_TYPE].unique()
        self.assertEquals(columns, expected_columns)
        self.assertCountEqual(instance_type_list, instance_types_df)

    def test_spot_less_than_on_demand(self):
        spot_price = aws_pricing.get_spot_price('t3.large', 'us-east-1')
        on_demand_price = aws_pricing.get_on_demand_price('t3.large',
                                                          'us-east-1')
        self.assertLessEqual(spot_price, on_demand_price)
