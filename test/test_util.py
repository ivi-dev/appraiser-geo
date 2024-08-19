"""
Test the app's utility module.`
"""

import unittest
from unittest.mock import call, mock_open, patch

from src.util import print_dict, read_sorted, sort_neighborhoods


class TestUtil(unittest.TestCase):
    @patch('builtins.print')
    def test_print_dict_prints_a_dict_to_std_out_correctly(self, print):
        d = {'a': 1, 'b': {'c': 2}}
        print_dict(d)
        self.assertEqual(2, len(print.mock_calls))
        self.assertEqual(call('a: 1'), print.mock_calls[0])
        self.assertEqual(call('b: {\'c\': 2}'), print.mock_calls[1])

    @patch('src.util.open', mock_open(read_data='c\nb\na'))
    def test_read_sorted_returns_lines_of_file_in_asc_order(self):
        lines = read_sorted('file.txt')
        self.assertEqual(['a', 'b\n', 'c\n'], lines)

    def test_sort_neighborhoods_sorts_ascending(self):
        cities = {
            'City-1': {'neighborhoods': ['b', 'c', 'a']},
            'City-2': {},
        }
        cities = sort_neighborhoods(cities)
        self.assertEqual({
            'City-1': {'neighborhoods': ['a', 'b', 'c']},
            'City-2': {},
        }, cities)