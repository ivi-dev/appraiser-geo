"""
This module contains utilities for parsing the porogram's
command-line arguments.
"""

import argparse


def parser() -> argparse.ArgumentParser:
    """
    Return an instance of :class:`argparse.ArgumentParser` to
    process this program's command-line arguments.
    """

    arg_parser = argparse.ArgumentParser(
        description='Merge the content of files containing information about '
                    'populated places - cities and nighborhoods, formatted '
                    'according to the Appraiser\'s geographic classification '
                    'into a single structured string.'
    )
    arg_parser.add_argument(
        '--csv', 
        help='Path to the file containing CSV-formated geo data. '
             'If this is specified the "--cities" and "--neighborhoods" '
             'parameters are ignored.'
    )
    arg_parser.add_argument(
        '--cities', 
        help='Path to the file containing cities information. '
        'If "--csv" is specified this is ignored.'
    )
    arg_parser.add_argument(
        '--neighborhoods', 
        help='Path to the file containing neighborhood information. '
        'If "--csv" is specified this is ignored.'
    )
    arg_parser.add_argument(
        '--out', 
        default='geo.json', 
        help='Path to the file to write the merged geo data to. '
             'If not specified the data will go into geo.json in the '
             'current directory.'
    )
    return arg_parser


def parse() -> argparse.Namespace:
    """
    Return a :class:`argparse.Namespace` instance containing this program's 
    command-line arguments, parsed by the argument parser 
    returned by :func:`parser`.
    """

    arg_parser = parser()
    return arg_parser.parse_args()