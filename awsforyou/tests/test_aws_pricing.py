import unittest

import pandas as pd
import numpy as np

from awsforyou import aws_pricing


class TestAwsPricing(unittest.TestCase):

    def test_get_all_regions(self):
        regions = aws_pricing.get_all_regions()
        self.assertIsNotNone(regions)
        self.assertGreater(len(regions), 0)

    def test_get_spot_pricing(self):
        price = aws_pricing.get_spot_price(['t3.large',
                                            'c5.18xlarge'], 'us-east-1')
        self.assertIsInstance(price, pd.DataFrame)
        self.assertIsNotNone(price)

    def test_get_on_demand_pricing(self):
        price = aws_pricing.get_on_demand_price(['t3.large',
                                                 'c5.18xlarge'], 'us-east-1')
        t3_price_exp = 0.0832
        c5_price_exp = 3.0600
        t3_price = price[price['instance_type'] ==
                         't3.large']['on_demand_price'].item()
        c5_price = price[price['instance_type'] ==
                         'c5.18xlarge']['on_demand_price'].item()

        self.assertEquals(t3_price, t3_price_exp)
        self.assertEquals(c5_price, c5_price_exp)

    def test_get_all_pricing_multiple_instance(self):
        instance_type_list = ['c5.18xlarge', 'm5a.large', 'c5.xlarge']
        price_df = aws_pricing.get_instance_pricing(instance_type_list)
        self.assertIsInstance(price_df, pd.DataFrame)
        columns = list(price_df.columns)
        expected_columns = [aws_pricing.DF_COL_INSTANCE_TYPE,
                            aws_pricing.DF_COL_REGION,
                            aws_pricing.DF_COL_SPOT_PRICE,
                            aws_pricing.DF_COL_ON_DEMAND_PRICE]

        instance_types_df = price_df[aws_pricing.DF_COL_INSTANCE_TYPE].unique()
        self.assertEquals(columns, expected_columns)
        self.assertCountEqual(instance_type_list, instance_types_df)

    def test_spot_less_than_on_demand(self):
        instance_type_list = ['c5.18xlarge', 'm5a.large', 'c5.xlarge']
        price_df = aws_pricing.get_instance_pricing(instance_type_list)
        spot_prices = price_df[aws_pricing.DF_COL_SPOT_PRICE]
        on_demand_prices = price_df[aws_pricing.DF_COL_ON_DEMAND_PRICE]
        compare_results = spot_prices <= on_demand_prices

        self.assertTrue(np.all(compare_results))
