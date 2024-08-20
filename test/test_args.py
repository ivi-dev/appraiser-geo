# pylint: skip-file

from argparse import Namespace
import unittest

from unittest.mock import patch

from src import args


class TestArgs(unittest.TestCase):
    prog_args_def_out = [
        'prog.exe', 
        '--cities', 
        'cities.txt', 
        '--neighborhoods', 
        'neighborhoods.txt'
    ]
    prog_args_cust_out = [
        'prog.exe', 
        '--cities', 
        'cities.txt', 
        '--neighborhoods', 
        'neighborhoods.txt', 
        '--out', 
        'out.json'
    ]
    prog_args_csv_in = [
        'prog.exe', 
        '--csv', 
        'geo.csv'
    ]

    @patch('sys.argv', prog_args_def_out)
    def test_parse_parses_args_default_out_path(self):
        prog_args = args.parse()
        self.assertEqual(
            Namespace(
                csv=None,
                cities='cities.txt', 
                neighborhoods='neighborhoods.txt', 
                out='geo.jso'
            ), 
            prog_args
        )

    @patch('sys.argv', prog_args_cust_out)
    def test_parse_parses_args_custom_out_path(self):
        prog_args = args.parse()
        self.assertEqual(
            Namespace(
                csv=None,
                cities='cities.txt', 
                neighborhoods='neighborhoods.txt', 
                out='out.json'
            ), 
            prog_args
        )

    @patch('sys.argv', prog_args_csv_in)
    def test_parse_parses_args_csv_path(self):
        prog_args = args.parse()
        self.assertEqual(
            Namespace(
                csv='geo.csv',
                cities=None, 
                neighborhoods=None, 
                out='geo.json'
            ), 
            prog_args
        )