"""
Unittests for benchmark_runner.py
"""

import mock
import os
import pandas as pd
import unittest

from awsforyou import benchmark_runner as bench


class TestGetData(unittest.TestCase):
    """
    Test cases for the function get_data
    """
    def test_get_data(self):
        """
        Testing the get data funciton
        """
        data = bench.get_data()
        x_train, y_train, x_test, y_test = data
        self.assertEqual((60000, 784), x_train.shape)
        self.assertEqual((60000, 10), y_train.shape)
        self.assertEqual((10000, 784), x_test.shape)
        self.assertEqual((10000, 10), y_test.shape)


class TestRunBenchmark(unittest.TestCase):
    """
    Test cases for the function run_benchmark
    """
    def test_runtime(self):
        """
        Check if output is indeed number of seconds
        """
        runtime = bench.run_benchmark(aws=False)
        self.assertIsInstance(runtime, float)

    def test_aws_true(self):
        """
        Uses mock to simulate the situation where aws = Test
        """

        mock_instancetype_region = \
            {
                'instancetype': 'someinstancetype', 'region': 'someregion'
            }
        mocked_aws_metadata = \
            mock.patch('awsforyou.aws_metadata.get_instance',
                       return_value=mock_instancetype_region)

        mocked_aws_metadata.start()
        runtime = bench.run_benchmark(aws=True)
        scorecard = pd.read_csv('./aws-scorecard.csv')
        dict_scorecard = scorecard.to_dict(orient='records')[0]
        dict_scorecard = \
            {
                'instancetype': dict_scorecard['instancetype'],
                'region': dict_scorecard['region']
            }
        mocked_aws_metadata.stop()
        self.assertEqual(mock_instancetype_region, dict_scorecard)


class TestWriteScorecard(unittest.TestCase):
    """
    Test write_scorecard function
    """
    def test_writescorecard_exist(self):
        """
        Test write_scorecard when there is an existing CSV.
        """
        gold_dict = {
            'datetime': '2019-06-03 22:13:45',
            'RAM': 8,
            'arch': 'X86_64',
            'bits': 64,
            'brand': 'Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz',
            'count': 8,
            'cpuinfo_version': '[5, 0, 0]',
            'extended_model': 8,
            'family': 6,
            'flags': "['some', 'flag', 'here']",
            'hz_actual': '1.8000 GHz',
            'hz_actual_raw': '[1800000000, 0]',
            'hz_advertised': '1.6000 GHz',
            'hz_advertised_raw': '[1600000000, 0]',
            'instancetype': 'local-machine',
            'l2_cache_associativity': '0x100',
            'l2_cache_line_size': 6,
            'l2_cache_size': 64,
            'l3_cache_size': '256 KB',
            'model': 142,
            'python_version': '3.6.7.final.0 (64 bit)',
            'raw_arch_string': 'x86_64',
            'region': 'local-machine',
            'runtime': 40.49512386322022,
            'stepping': 10,
            'timezone': 'UTC',
            'vendor_id': 'GenuineIntel'
            }
        existing_csv = pd.DataFrame([gold_dict])
        existing_csv.set_index('datetime', inplace=True)
        existing_csv.to_csv('./aws-scorecard.csv')
        bench.write_scorecard(gold_dict)
        scorecard = pd.read_csv('./aws-scorecard.csv')
        dict_scorecard = scorecard.to_dict(orient='records')
        self.assertEqual([gold_dict, gold_dict], dict_scorecard)

    def test_writescorecard_notexist(self):
        """
        Test write_scorecard when there is no existing CSV.
        """
        gold_dict = {
            'datetime': '2019-06-03 22:13:45',
            'RAM': 8,
            'arch': 'X86_64',
            'bits': 64,
            'brand': 'Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz',
            'count': 8,
            'cpuinfo_version': '[5, 0, 0]',
            'extended_model': 8,
            'family': 6,
            'flags': "['some', 'flag', 'here']",
            'hz_actual': '1.8000 GHz',
            'hz_actual_raw': '[1800000000, 0]',
            'hz_advertised': '1.6000 GHz',
            'hz_advertised_raw': '[1600000000, 0]',
            'instancetype': 'local-machine',
            'l2_cache_associativity': '0x100',
            'l2_cache_line_size': 6,
            'l2_cache_size': 64,
            'l3_cache_size': '256 KB',
            'model': 142,
            'python_version': '3.6.7.final.0 (64 bit)',
            'raw_arch_string': 'x86_64',
            'region': 'local-machine',
            'runtime': 40.49512386322022,
            'stepping': 10,
            'timezone': 'UTC',
            'vendor_id': 'GenuineIntel'
            }
        bench.write_scorecard(gold_dict)
        scorecard = pd.read_csv('./aws-scorecard.csv')
        dict_scorecard = scorecard.to_dict(orient='records')[0]
        self.assertEqual(gold_dict, dict_scorecard)

    def test_keyerror(self):
        """
        Test write_scorecard for when the variable results_dict passed
        does not contain the correct key-value pair
        """
        os.remove("aws-scorecard.csv")
        dummy_dict = {'foo': 'bar'}
        self.assertRaises(KeyError, bench.write_scorecard, dummy_dict)
