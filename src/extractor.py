"""
This module contains utilities for extracting CSV-formatted 
geo data to be further processed by the program.
"""

import csv
import re
from typing import Iterable, Mapping

from src.constants import ALL, NEIGHBORHOODS_KEY
from src.translit import Transliterator
from src.types import City

# Regex
AREA_GROUP = 'area'
AREA_REGEX = f'(?P<{AREA_GROUP}>[A-Z]{{3}}[0-9]{{2}})'

# Keys
GL1_KEY = 'gl1'
GL2_KEY = 'gl2'

# Misc
CITY_LINE_SEPARATOR = 5 * '.'

transliter = Transliterator(
    locale='bg',
    corr_table={
        'софиа': 'София',
        'велико тарново': 'Велико Търново'
    }
)

# Types
GeoSplit = tuple[Iterable[str], Mapping[str, Iterable[str]]]



def extract_geo_data(path: str) -> GeoSplit:
    """
    Extract the geo data from the CSV file at ``path`` 
    into a 2-tuple. The first element of that tuple
    is an iterable of strings, where each string carries
    information about a city/town, along with its geogrpahy
    level ID(s) and is formatted according to the 
    :ref:`city-format` specification. E.g.::

        [
            ...
            'София..............(GL1: sofia)',
            'Пловдив............(GL1: plovdiv)',
            'Хаджидимово........(GL1: southwestern; GL2: BLG52)',
            ...
        ]
    
    The second tuple element is a mapping of the names of
    those cities in the first tuple element that have 
    listed neighborhoods and the neighorhood list itself.
    E.g.::

        {
            ...
            'София': ['Изгрев', 'Гоце Делчев', 'Борово', ...],
            'Пловдив': ['Коматево', 'Беломорски', 'Остромила', ...],
            ...
        }

    For a sample geo CSV check :ref:`csv-format`.
    """

    with open(path, newline='', encoding='utf8') as file:
        reader = csv.reader(file)
        data = {}
        for i, row in enumerate(reader):
            if i > 0:
                gl1, col2, col3 = row
                town = re.match(AREA_REGEX, col2)
                if not town: # City
                    city_name = transliter.translit(gl1.replace('_', ' ').title())
                    neigh = f'--{col3.title()}--' if col3.lower() == ALL.lower() else col3
                    if city_name not in data:
                        data[city_name] = {GL1_KEY: gl1, NEIGHBORHOODS_KEY: [neigh]}
                    else:
                        data[city_name][NEIGHBORHOODS_KEY].append(neigh)
                else: # Town
                    city_name = transliter.translit(col3.replace('_', ' ').title())
                    if city_name not in data:
                        data[city_name] = {GL1_KEY: gl1, GL2_KEY: col2}
                    else:
                        data[city_name].update({GL1_KEY: gl1, GL2_KEY: col2})
    return split_geo_data(data)


def split_geo_data(data: Mapping[str, City]) -> GeoSplit:
    """
    Split the provided geo ``data`` into a 2-tuple containing
    city and neighborhood data respectively. The cities are 
    formatted according to the :doc:`data_format`.
    """

    cities, neighborhoods = [], {}
    for city, info in data.items():
        if NEIGHBORHOODS_KEY in info: # City
            line = f'{city}{CITY_LINE_SEPARATOR}' \
                   f'(GL1: {info[GL1_KEY]}'
            if GL2_KEY in info: # Edge case: a city has a GL2 ID
                line += f'; GL2: {info[GL2_KEY]}'
            line += ')'
            cities.append(line)
            neighborhoods[city] = info[NEIGHBORHOODS_KEY]
        else: # Town
            cities.append(
                f'{city}{CITY_LINE_SEPARATOR}'
                f'(GL1: {info[GL1_KEY]}; GL2: {info[GL2_KEY]})'
            )
    return sorted(cities), neighborhoods
