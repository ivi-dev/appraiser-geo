"""
This is the program's entry module intended to be invoked by a command-line.
It reads user-specified arguments and uses its utilities to process the 
pointed-to files containing populated places - cities, towns and neighborhoods, 
formatted according to the :doc:`geo_classification`, and produces a structured text 
file containing compact presentations of those places along with their geography 
level(s) and constituent areas.
"""

import json
import sys
from typing import Mapping

from src.mapper import map_geo, map_neighborhoods, map_polygons, update_suburbs
from src.types import PartitionedCity

from src.util import read_sorted
from src.args import parse as parse_args
from src.extractor import extract_geo_data


def write_cities_json(cities: Mapping[str, PartitionedCity], path: str) -> None:
    """
    Write a JSON dump of the specified ``cities`` data
    to a file at ``path``.
    """

    with open(path, 'wt', encoding='utf8') as file:
        file.write(json.dumps(cities, indent=4, ensure_ascii=False))


if __name__ == '__main__': # pragma: no cover
    prog_args = parse_args()
    in_csv = prog_args.csv
    in_cities = prog_args.cities
    in_neighborhoods = prog_args.neighborhoods
    in_polygons = prog_args.polygons
    out_path = prog_args.out
    if in_csv: # Work on the specified CSV file
        cities_, in_neighborhoods = extract_geo_data(in_csv)
    elif in_cities: # Work on the specified TEXT files
        cities_ = read_sorted(in_cities)
    else:
        print(
            'ERROR: Please provide either a CSV or a '
            'pair of cities and neighborhood files. '
            'If you need help, run the program with the '
            '-h option.'
        )
        sys.exit(1)
    cities_ = map_geo(cities_)
    cities_ = map_neighborhoods(cities_, in_neighborhoods)
    cities_ = map_polygons(cities_, *in_polygons)
    cities_ = update_suburbs(cities_)
    write_cities_json(cities_, out_path)
