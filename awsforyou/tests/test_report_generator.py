import os
import unittest

import pandas as pd

from awsforyou.report_generator import generate_report

TEST_REPORT = 'https://tinyurl.com/yyq8krf8'


class ReportGeneratorTest(unittest.TestCase):

    def setUp(self):
        self.test_report_data = pd.read_csv(TEST_REPORT)

    def test_report_generated(self):
        report_file_name = generate_report(self.test_report_data)
        file_exists = os.path.isfile(report_file_name)
        self.assertTrue(file_exists)

    def test_report_file_name(self):
        report_file_name = generate_report(self.test_report_data)
        file_html = report_file_name.endswith('.html')
        self.assertTrue(file_html)
