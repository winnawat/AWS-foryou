"""
Unittests for aws_metadata.py
"""

import mock
import os
import pandas as pd
from requests.models import Response
import unittest
from unittest.mock import Mock

from awsforyou import aws_metadata


class TestGetInstance(unittest.TestCase):
    """
    Test cases for the function get_instance
    """
    def test_get_instance(self):
        """
        Testing the request function that fetches AWS metadata
        """
        mock_response_json = \
            {
                'instanceType': 'someinstancetype', 'region': 'someregion'
            }
        mock_response = unittest.mock.Mock(spec=Response)
        mock_response.json.return_value = mock_response_json

        mock_request = mock.patch('requests.get',
                                  return_value=mock_response)
        mock_request.start()

        dict = aws_metadata.get_instance()

        mock_request.stop()
        expected_returned_dict = \
            {
                'instancetype': 'someinstancetype', 'region': 'someregion'
            }
        self.assertEqual(expected_returned_dict, dict)
