"""
This module contains utilities for mapping places
to their associated data entities, e.g. places to 
GeoJSON polygons, cities and towns to geography levels, 
cities to their neighborhoods etc.
"""


import copy
import json
import re
from typing import Iterable, Mapping, Optional
from src.constants import ALL, DEFAULT_ALL, GEO_JSON_KEY, IS_CITY_KEY, IS_SUBURBS_KEY, NEIGHBORHOODS_KEY, SHORTCUT_CITY_KEY, SHORTCUT_KEY, SHORTCUT_NEIGHBORHOOD_KEY, SUBURBAN_NEIGHBORHOOD_NAME
from src.constants import AREA_NAMES, CITY_DELIM_REGEX, CITY_NAME_GROUP, CITY_NAME_REGEX, \
                          CITY_REGEX, GEO_KEY, GEO_LEVEL_1_GROUP, GEO_LEVEL_1_KEY,        \
                          GEO_LEVEL_2_GROUP, GEO_LEVEL_2_KEY
from src.types import CitySuburbs, FullCity, GeoCity, PartitionedCity, Polygons, \
                      RawPolygonData, RawPolygonDataItem
from src.extractor import transliter


def get_raw_polygon_data(*paths: str) -> RawPolygonData:
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
                GEO_JSON_KEY: feature,
            }
            if 'geography_level_2' in feature['properties']:
                data['geo']['level-2'] = feature['properties']['geography_level_2']
            if 'geography_level_2_bg' in feature['properties']:
                data['geo']['level-2-bg'] = feature['properties']['geography_level_2_bg']
            polygons.append(data)
    return polygons


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
                    neighborhood_ = DEFAULT_ALL if \
                                    neighborhood.lower() == ALL.lower() else \
                                    neighborhood
                    cities[city_name][NEIGHBORHOODS_KEY].append(neighborhood_)
    else: # A map provided
        for city_name, neighborhoods_ in neighborhoods.items():
            cities[city_name][NEIGHBORHOODS_KEY] = neighborhoods_
    return cities


def get_unmapped_polygons(
    polygons: RawPolygonData,
    mapped_polys: list[int]
) -> Iterable[RawPolygonDataItem]:
    """
    Return the polygon data items that still
    haven't been mapped to places.
    """

    unmapped_polys = []
    for i, poly in enumerate(polygons):
        if i not in mapped_polys:
            unmapped_polys.append(poly)
    return unmapped_polys


def get_unmapped_neighborhoods(
    unmapped_polys: Iterable[RawPolygonDataItem]
) -> Mapping[str, Iterable[Mapping[str, str | Polygons]]]:
    """
    Return a map of the cities, identified by their level 
    1 geo's and their neighborhoods that haven't still been
    mapped to polygons.
    """

    unmapped_neighborhoods = {}
    for poly in unmapped_polys:
        lvl_1 = poly['geo']['level-1']
        if 'level-2' in poly['geo']:
            lvl_2 = poly['geo']['level-2']
            lvl_2_bg = poly['geo']['level-2-bg']
            neigh = {
                'name': lvl_2_bg, 
                GEO_JSON_KEY: poly[GEO_JSON_KEY]
            }
            if lvl_2 != 'all':
                if lvl_1 not in unmapped_neighborhoods:
                    unmapped_neighborhoods[lvl_1] = [neigh]
                else:
                    unmapped_neighborhoods[lvl_1].append(neigh)
    # Sort the neighborhoods
    for city_lvl_1 in unmapped_neighborhoods:
        unmapped_neighborhoods[city_lvl_1] = sorted(
            unmapped_neighborhoods[city_lvl_1],
            key=lambda city: city['name']
        )
    return unmapped_neighborhoods


def find_town_polygon_data(
    level_1: str,
    level_2: Optional[str],
    polygons: RawPolygonData
) -> tuple[RawPolygonDataItem, int]:
    """
    Return a two-tuple of the raw polygon data item matching
    the specified ``level_1`` and ``level_2``, and the index
    of that item in ``polygons``.
    """

    idx = 0
    for poly_data in polygons:
        if poly_data['geo']['level-1'] == level_1:
            if 'level-2' in poly_data['geo'] and \
                poly_data['geo']['level-2'] == level_2:
                return poly_data, idx
        idx += 1
    return None


def map_areas_to_polygons(
    unmapped_polys: Iterable[RawPolygonDataItem],
    cities: list[str],
    places: Mapping[str, PartitionedCity]
):
    """
    Map the geographical area to their polygons.
    """

    # print(json.dumps(places, indent=4, ensure_ascii=False))
    for poly in unmapped_polys:
        clean_name = poly['geo']['level-1'].replace('_', ' ').title()
        place_name = transliter.translit(clean_name)
        is_area = poly['geo']['level-1'] not in cities \
                    and place_name not in cities
        if 'level-2' not in poly['geo'] and is_area: # It's an AREA
            places[AREA_NAMES[poly['geo']['level-1']]] = {
                'geography': {
                    'level-1': poly['geo']['level-1']
                },
                GEO_JSON_KEY: poly[GEO_JSON_KEY],
                'isArea': True
            }


def map_cities_to_polygons(
    unmapped_polys: Iterable[RawPolygonDataItem],
    cities: list[str],
    places: Mapping[str, PartitionedCity]
):
    """
    Map the still unmapped whole cities (those without neighborhoods 
    listed in the raw polygon data) to their poylgons.
    """

    for poly in unmapped_polys:
        clean_name = poly['geo']['level-1'].replace('_', ' ').title()
        place_name = transliter.translit(clean_name)
        is_city = poly['geo']['level-1'] in cities or place_name in cities
        if 'level-2' not in poly['geo'] and is_city: # It's a CITY
            for _, data in places.items(): # Add that city's GeoJSON
                if data['geography']['level-1'] == poly['geo']['level-1']:
                    data[GEO_JSON_KEY] = poly[GEO_JSON_KEY]
                    data[ IS_CITY_KEY] = True
                    break


def map_towns_to_polygons(
    polygons: RawPolygonData,
    places: Mapping[str, PartitionedCity]
) -> Iterable[int]:
    """
    Map towns to their polygons.
    """

    mapped_towns = []
    for _, place_data in places.items():
        level_1 = place_data['geography']['level-1']
        level_2 = place_data['geography']['level-2'] if \
                'level-2' in place_data['geography'] else \
                None
        data = find_town_polygon_data(level_1, level_2, polygons)
        if data is not None:
            poly, idx = data[0], data[1]
            place_data[GEO_JSON_KEY] = poly[GEO_JSON_KEY]
            place_data[ IS_CITY_KEY] = False
            mapped_towns.append(idx)
    return mapped_towns


def map_neighborhoods_to_polygons(
    unmapped_neighborhoods: Mapping[str, Iterable[Mapping[str, str | Polygons]]],
    places: Mapping[str, PartitionedCity]
) -> Iterable[str]:
    """
    Map the still unmapped neighborhoods to their poylgons.
    """

    cities = []
    for city_lvl_1, data in unmapped_neighborhoods.items():
        for place_name, place_data in places.items():
            # COMMON CASE: There's a match on geo level 1
            if place_data['geography']['level-1'] == city_lvl_1:
                place_data['neighborhoods'] = data
                cities.append(place_data['geography']['level-1'])
            else:
                # The still unmapped neighborhoods' names
                neigh_names = [
                    neigh['name']
                    for neigh
                    in data
                ]
                # EDGE CASE for "Велико Търново": There's no match on geo level 1
                if 'neighborhoods' in place_data and \
                    not isinstance(place_data['neighborhoods'][0], dict):
                    # Check the neighborhood lists for being "close enough" -
                    # there's only one excess item "Select All" in the places
                    # record's list, the other items are the same
                    neigh_diff = list(
                        set(place_data['neighborhoods']) - set(neigh_names)
                    )
                    neigh_list_identical = len(neigh_diff) == 1 and \
                                            neigh_diff[0] == DEFAULT_ALL
                    if neigh_list_identical:
                        place_data['neighborhoods'] = \
                            unmapped_neighborhoods[city_lvl_1]
                        cities.append(place_name)
                        place_data[ IS_CITY_KEY] = True
                        break
    return cities


def map_polygons(
    places: Mapping[str, PartitionedCity],
    *polygon_paths: Iterable[str]
) -> Mapping[str, FullCity]:
    """
    Map each of the ``places`` to its GeoJSON polygons.

    If ``polygon_paths`` is an iterable of strings, 
    it's assumed that those are file paths, and polygon 
    data will be derived from them.
    """

    polygons = get_raw_polygon_data(*polygon_paths)
    mapped_polys = map_towns_to_polygons(polygons, places)
    unmapped_polys = get_unmapped_polygons(polygons, mapped_polys)
    unmapped_neighborhoods = get_unmapped_neighborhoods(unmapped_polys)
    cities = map_neighborhoods_to_polygons(unmapped_neighborhoods, places)
    map_cities_to_polygons(unmapped_polys, cities, places)
    map_areas_to_polygons(unmapped_polys, cities, places)
    return places


def update_suburbs(cities: Mapping[str, FullCity]) -> Mapping[str, FullCity]:
    """
    Create new entries in the specified ``cities`` nomenclature
    to reflect the associated cities' suburban areas.
    """

    def get_suburb_data() -> dict[str, int]:
        """
        Return a map of the names of the cities with
        declared suburban areas and the index of the 
        "Suburbs" option in thier list of neighborhoods.
        """

        data_ = {} # Format: {'<CITY_NAME>': <SUBURB_OPTION_IDX>}
        for city, data in cities.items():
            if NEIGHBORHOODS_KEY in data:
                for i, neigh in enumerate(data[NEIGHBORHOODS_KEY]):
                    if neigh['name'] == SUBURBAN_NEIGHBORHOOD_NAME:
                        data_[city] = i
                        break
        return data_

    def create_suburb_entry(city_name: str) -> CitySuburbs:
        """
        Create a new 'suburbs' nomenclature entry.
        """

        entry = copy.deepcopy(cities[city_name])
        del entry[NEIGHBORHOODS_KEY]
        del entry[IS_CITY_KEY]
        entry[SHORTCUT_KEY] = {}
        entry[SHORTCUT_KEY][SHORTCUT_CITY_KEY] = city_name
        entry[SHORTCUT_KEY][SHORTCUT_NEIGHBORHOOD_KEY] = SUBURBAN_NEIGHBORHOOD_NAME
        entry[IS_SUBURBS_KEY] = True
        return entry
    
    def update_cities(data: dict[str, int]):
        """
        Update the cities nomenclature with the associated cities'
        suburban data.
        """

        for city, _ in data.items():
            cities[f'{city}-{SUBURBAN_NEIGHBORHOOD_NAME}'] = create_suburb_entry(city)

    data = get_suburb_data()
    update_cities(data)
    cities = dict(sorted(cities.items()))
    return cities
