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
from src.types import GeoCity, PartitionedCity, FullCity, RawPolygonData, RawPolygonDataItem

from src.util import read_sorted, sort_neighborhoods
from src.args import parse as parse_args
from src.extractor import NEIGHBORHOODS_KEY, extract_geo_data, transliter


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


def map_geo(cities: Iterable[str]) -> Mapping[str, GeoCity]:
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
    cities: Mapping[str, GeoCity],
    neighborhoods: str | Mapping[str, Iterable[str]]
) -> Mapping[str, PartitionedCity]:
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


def map_polygons(
    places: Mapping[str, PartitionedCity],
    polygon_paths: Iterable[str]
) -> Mapping[str, FullCity]:
    """
    Map each of the ``places`` to its GeoJSON polygons.

    If ``polygon_paths`` is an iterable of strings, 
    it's assumed that those are file paths, and polygon 
    data will be derived from them.
    """

    def place_matches(
        place: RawPolygonDataItem,
        places: Mapping[str, PartitionedCity],
        place_name: str
    ) -> bool:
        """
        Return whether the specified ``place`` matches 
        the specified ``geo_level_1`` and optionally 
        ``geo_level_2`` and ``geo_level_2_bg``.
        """

        geo_level_1 = places[place_name]['geography']['level-1']
        geo_level_2 = places[place_name]['geography']['level-2'] if \
                     'level-2' in places[place_name]['geography'] else \
                     None
        geo_level_2_bg = place_name

        # What props exist on this polygon data item
        poly_place_has_level_2 = 'level-2' in place['geo']
        poly_place_has_level_2_bg = 'level-2-bg' in place['geo']

        # Matches by various props
        level_1_match = place['geo']['level-1'] == geo_level_1
        level_2_match = True
        level_2_bg_match = True
        
        # Match on various props conditionally
        if poly_place_has_level_2:
            level_2_match = place['geo']['level-2'] == geo_level_2
        if poly_place_has_level_2_bg:
            level_2_bg_match = place['geo']['level-2-bg'] == geo_level_2_bg

        if geo_level_2_bg == 'Аврен':
            print(geo_level_1, geo_level_2, geo_level_2_bg)
         
        # A match means all props (if exist) match
        return level_1_match and level_2_match and level_2_bg_match
    
    def find_polygon_data(
        data: RawPolygonData,
        places: Mapping[str, PartitionedCity],
        place_name: str
    ) -> RawPolygonDataItem:
        """
        Return the polygon data item of the place identified 
        by the specified ``geo_level_1``, ``geo_level_2`` 
        and ``geo_level_2_bg``.
        """

        # return filter(
        #     lambda place: place_matches(
        #         place,
        #         places,
        #         place_name
        #     ),
        #     data
        # )
        for poly in data:
            place = places[place_name]

    polygons_ = get_polygons(*polygon_paths)
    mapped_polys = [] # Indices of mapped polygons
    for place_name, place_data in places.items():
        # Find this place's polygon data
        level_1 = place_data['geography']['level-1']
        level_2 = place_data['geography']['level-2'] if \
                  'level-2' in place_data['geography'] else \
                  None
        idx = 0
        for poly_data in polygons_:
            if poly_data['geo']['level-1'] == level_1:
                if 'level-2' in poly_data['geo']:
                    if poly_data['geo']['level-2'] == level_2:
                        place_data['polygons'] = poly_data['coordinates']
                        mapped_polys.append(idx)
                        break
            idx += 1

    # Get the polygons still not mapped to places
    not_mapped_polys = []
    for i, poly in enumerate(polygons_):
        if i not in mapped_polys:
            not_mapped_polys.append(poly)
    
    # Get the still unmapped neighborhoods
    neigh = {}
    for poly in not_mapped_polys:
        lvl_1 = poly['geo']['level-1']
        if 'level-2' in poly['geo']:
            lvl_2 = poly['geo']['level-2']
            if lvl_1 not in neigh:
                neigh[lvl_1] = []
            else:
                neigh[lvl_1].append(lvl_2)
    # TODO: Map them...

    print(
        'STILL UNMAPPED NEIGHBORHOODS', 
        json.dumps(neigh, indent=4)
    )
    print(
        'STILL UNMAPPED NEIGHBORHOODS', 
        json.dumps(
            [
                {
                    'city': neigh_, 
                    'neighborhoods': len(neigh[neigh_])
                } 
                for neigh_ 
                in neigh
            ], 
            indent=4
        )
    )

    # Get the still unmapped areas
    areas = []
    for poly in not_mapped_polys:
        lvl_1 = poly['geo']['level-1']
        if lvl_1 not in neigh:
            areas.append(lvl_1)
    # TODO: Map them...

    print('STILL UNMAPPED AREAS', json.dumps(areas, indent=4))

    return places


def get_polygons(*paths: str) -> RawPolygonData:
    """
    Parse and return the polygon data contained in the
    GeoJSON files at ``paths``.
    """

    polygons = []
    for path in paths:
        with open(path, 'rt', encoding='utf8') as file:
            cont = file.read()
        data = json.loads(cont)
        for feature in data['features']:
            data = {
                'geo': {
                    'level-1': feature['properties']['geography_level_1']
                },
                'coordinates': feature['geometry']['coordinates'],
            }
            if 'geography_level_2' in feature['properties']:
                data['geo']['level-2'] = feature['properties']['geography_level_2']
            polygons.append(data)
    return polygons


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
    cities_ = map_polygons(cities_, in_polygons)

    # with open('C:\\users\\iliyanvidev\\desktop\\out-full-places.json', 'wt', encoding='utf8') as file:
    #     file.write(json.dumps(cities_, indent=4, ensure_ascii=False))

    # cities_ = sort_neighborhoods(cities_)
    # write_cities_json(cities_, out_path)
