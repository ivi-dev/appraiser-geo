"""
This is the program's entry module intended to be invoked by a command-line.
It reads user-specified arguments and uses its utilities to process the 
pointed-to files containing populated places - cities, towns and neighborhoods, 
formatted according to the :doc:`geo_classification`, and produces a structured text 
file containing compact presentations of those places along with their geography 
level(s) and constituent areas.
"""

import re
import json
import sys
from typing import Iterable, Mapping

from src.constants import ALL
from src.types import City, PartialCity

from src.util import read_sorted, sort_neighborhoods
from src.args import parse as parse_args
from src.extractor import NEIGHBORHOODS_KEY, extract_geo_data


# Regex
CITY_NAME_GROUP = 'city_name'
CITY_DELIM_GROUP = 'delim'
GEO_LEVEL_1_GROUP = 'gl1'
GEO_LEVEL_2_GROUP = 'gl2'
CITY_REGEX = fr'(?P<{CITY_NAME_GROUP}>.+?)'                  \
             fr'(?P<{CITY_DELIM_GROUP}>\.+?)'                \
             fr'\(GL1:\s*(?P<{GEO_LEVEL_1_GROUP}>.+?)'       \
             fr'(;\s*GL2:\s*(?P<{GEO_LEVEL_2_GROUP}>.+?))*\)'
CITY_DELIM_REGEX = r'^\s*-+\s*$'
CITY_NAME_REGEX = f'^(?P<{CITY_NAME_GROUP}>.+):$'

# Keys
GEO_KEY = 'geography'
GEO_LEVEL_1_KEY = 'level-1'
GEO_LEVEL_2_KEY = 'level-2'


def map_geo(cities: Iterable[str]) -> Mapping[str, PartialCity]:
    """
    Map the provided city names to their geography level(s).

    The cities in the specified iterable ``cities`` is expected
    to contain strings that include a city/town's name and its
    geography level 1 *(GL1)* and, if applicable, geography level 2 
    *(GL2)* IDs. The expected format is::

        <City name>....(GL1: <geo level 1>[; GL2: <geo level 2>])
    """

    clean = {}
    for city in cities:
        data = re.search(CITY_REGEX, city)
        if data:
            city_name = data.group(CITY_NAME_GROUP).strip()
            level_1 = data.group(GEO_LEVEL_1_GROUP)
            level_2 = data.group(GEO_LEVEL_2_GROUP)
            clean[city_name] = {GEO_KEY: {GEO_LEVEL_1_KEY: level_1}}
            if level_2:
                clean[city_name][GEO_KEY][GEO_LEVEL_2_KEY] = level_2
    return clean


def map_neighborhoods(
    cities: Mapping[str, PartialCity],
    neighborhoods: str | Mapping[str, Iterable[str]]
) -> Mapping[str, City]:
    """
    Map each of the ``cities`` to its neighborhoods.

    If ``neighborhoods`` is a string, it's assumed that
    it's a file path, and the city's neighborhoods will 
    be derived from it. The file will be treated as a flat 
    text one and its content is expected to be formatted 
    acccording to the :doc:`data_format` guidelines.

    If ``neighborhoods`` is a map, then its expected to contain
    city names mapped to their associated neighborhood lists. 
    """

    if isinstance(neighborhoods, str): # File path provided
        neighborhoods_ = []
        with open(neighborhoods, 'rt', encoding='utf8') as file:
            neighborhoods_ = file.readlines()
        delim_start, delim_end = False, False
        for neighborhood in neighborhoods_:
            # City's openning char sequence not yet encountered
            if not delim_start and not delim_end:
                if re.match(CITY_DELIM_REGEX, neighborhood): # Mark start of city name
                    delim_start = True
                    continue
            elif delim_start and not delim_end: # City's openning char sequence already encountered
                if re.match(CITY_DELIM_REGEX, neighborhood): # Mark the end of city name
                    delim_end = True
                else: # Try to get the city's name
                    city_match = re.match(CITY_NAME_REGEX, neighborhood)
                    if city_match:
                        city_name = city_match.group(CITY_NAME_GROUP).strip()
                        cities[city_name][NEIGHBORHOODS_KEY] = []
            else: # A neighborhood
                if re.match(CITY_DELIM_REGEX, neighborhood): # Mark the end of neighborhoods
                    delim_start = True
                    delim_end = False
                    continue
                neighborhood = neighborhood.strip()
                if neighborhood != '': # The neighborhood's name
                    neighborhood_ = f'--{neighborhood.title()}--' if \
                                    neighborhood.lower() == ALL.lower() else \
                                    neighborhood
                    cities[city_name][NEIGHBORHOODS_KEY].append(neighborhood_)
    else: # A map provided
        for city_name, neighborhoods_ in neighborhoods.items():
            cities[city_name][NEIGHBORHOODS_KEY] = neighborhoods_
    return cities


def write_cities_json(cities: Mapping[str, City], path: str) -> None:
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
    out_path = prog_args.out
    if in_csv: # Work on the specified CSV file
        cities_, in_neighborhoods = extract_geo_data(in_csv)
    elif in_cities: # Work on the specified TEXT files
        cities_ = read_sorted(in_cities)
    else:
        print(
            'ERROR: Please provide either a CSV or a '
            'pair of cities or neighborhood files. '
            'For help run the program with the -h option.'
        )
        sys.exit(1)
    cities_ = map_geo(cities_)
    cities_ = map_neighborhoods(cities_, in_neighborhoods)
    cities_ = sort_neighborhoods(cities_)
    write_cities_json(cities_, out_path)
