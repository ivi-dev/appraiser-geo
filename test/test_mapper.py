# pylint: skip-file

import json
import unittest
from unittest.mock import mock_open, patch

from src.mapper import find_town_polygon_data, get_raw_polygon_data,       \
                       get_unmapped_neighborhoods,                         \
                       get_unmapped_polygons, map_areas_to_polygons,       \
                       map_cities_to_polygons, map_geo, map_neighborhoods, \
                       map_neighborhoods_to_polygons, map_polygons, map_towns_to_polygons


class TestMapper(unittest.TestCase):
    mock_geo_feature_1 = {
        'properties': {
            'geography_level_1': 'northeastern',
            'geography_level_2': 'VAR01',
            'geography_level_2_bg': 'Аврен',
            'prop': 'val',
        }
    }

    mock_geo_feature_2 = {
        'properties': {
            'geography_level_1': 'sofia',
            'prop': 'val',
        }
    }

    mock_geo_feature_3 = {
        'properties': {
            'geography_level_1': 'plovdiv',
            'prop': 'val',
        }
    }

    mock_geo_feature_4 = {
        'properties': {
            'geography_level_1': 'northeastern',
            'prop': 'val',
        }
    }

    mock_geo_feature_5 = {
        'properties': {
            'geography_level_1': 'sofia',
            'geography_level_2': 'Izgrev',
            'geography_level_2_bg': 'Изгрев',
            'prop': 'val',
        }
    }

    mock_geo_feature_6 = {
        'properties': {
            'geography_level_1': 'plovdiv',
            'geography_level_2': 'Komatevo',
            'geography_level_2_bg': 'Коматево',
            'prop': 'val',
        }
    }

    geo_json = {
        'features': [
            mock_geo_feature_1,
            mock_geo_feature_2,
            mock_geo_feature_3,
            mock_geo_feature_4,
            mock_geo_feature_5,
            mock_geo_feature_6,
        ]
    }

    mock_geo_json = json.dumps(
        geo_json, 
        indent=4, 
        ensure_ascii=False
    )

    mock_city_1 =  {
        'name': 'София',
        'geo-level-1': 'sofia',
        'neigh': [
            'Изгрев',
        ]
    }

    mock_city_2 =  {
        'name': 'Пловдив',
        'geo-level-1': 'plovdiv',
        'neigh': [
            'Коматево',
        ]
    }
    
    mock_neigh_data = f'''\
--------
{mock_city_1["name"]}:
--------

{"\n".join(mock_city_1["neigh"])}


---------
{mock_city_2["name"]}:
---------

{"\n".join(mock_city_2["neigh"])}
'''
    
    expected_mapped_neigh = {
        'София': {
            'geography': {
                'level-1': mock_city_1["geo-level-1"]
            }, 
            'neighborhoods': mock_city_1["neigh"]
        }, 
        'Пловдив': {
            'geography': {
                'level-1': mock_city_2["geo-level-1"]
            }, 
            'neighborhoods': mock_city_2["neigh"]
        }, 
        'Аврен': {
            'geography': {
                'level-1': 'northeastern', 
                'level-2': 'VAR01'
            }
        }
    }

    expected_mapped_places = {
        "София": {
            "geography": {
                'level-1': mock_city_1["geo-level-1"]
            },
            "neighborhoods": [
                {
                    "name": mock_city_1['neigh'][0],
                    "geoJSON": {
                        "properties": mock_geo_feature_5['properties']
                    }
                }
            ],
            "geoJSON": {
                "properties": {
                    "geography_level_1": mock_city_1["geo-level-1"],
                    "prop": "val"
                }
            },
            "isCity": True
        },
        "Пловдив": {
            "geography": {
                "level-1": mock_city_2["geo-level-1"]
            },
            "neighborhoods": [
                {
                    "name": mock_city_2['neigh'][0],
                    "geoJSON": {
                        "properties": mock_geo_feature_6['properties']
                    }
                }
            ],
            "geoJSON": {
                "properties": {
                    "geography_level_1": mock_city_2["geo-level-1"],
                    "prop": "val"
                }
            },
            "isCity": True
        },
        "Аврен": {
            "geography": {
                "level-1": mock_geo_feature_1['properties']['geography_level_1'],
                "level-2": mock_geo_feature_1['properties']['geography_level_2']
            },
            "geoJSON": {
                "properties": mock_geo_feature_1['properties']
            },
            "isCity": False
        },
        "Североизточна България": {
            "geography": {
                "level-1": mock_geo_feature_4['properties']['geography_level_1']
            },
            "geoJSON": {
                "properties": mock_geo_feature_4['properties']
            },
            "isArea": True
        }
    }

    @patch('src.mapper.open', mock_open(read_data=mock_geo_json))
    def test_get_raw_polygon_data_returns_parsed_polygon_data(self):
        data = get_raw_polygon_data('GeoJSON.json')
        self.assertEqual(len(self.geo_json['features']), len(data))
        for i, feature in enumerate(self.geo_json['features']):
            expected = {'level-1': feature['properties']['geography_level_1']}
            if 'geography_level_2' in feature['properties']:
               expected = {
                   **expected, 
                   **{'level-2': feature['properties']['geography_level_2']}
                }
            if 'geography_level_2_bg' in feature['properties']:
               expected = {
                   **expected, 
                   **{'level-2-bg': feature['properties']['geography_level_2_bg']}
                }
            self.assertEqual(expected, data[i]['geo'])

    def test_map_geo_returns_a_dict_of_place_data(self):
        cities = [
            'София....(GL1: sofia)',
            'Пловдив....(GL1: plovdiv)',
            'Аврен....(GL1: northeastern; GL2: VAR01)',
        ]
        mapped = map_geo(cities)
        self.assertEqual(
            {
                'Аврен': {
                    'geography': {
                        'level-1': 'northeastern', 
                        'level-2': 'VAR01'
                    }
                },
                'Пловдив': {
                    'geography': {
                        'level-1': 'plovdiv'
                    }
                },
                'София': {
                    'geography': {
                        'level-1': 'sofia'
                    }
                }
            }, 
            mapped
        )

    @patch('src.mapper.open', mock_open(read_data=mock_neigh_data))
    def test_map_neighborhoods_neigh_filepath_returns_cities_mapped_to_their_neighborhoods(self):
        cities = [
            f'{self.mock_city_1["name"]}....(GL1: {self.mock_city_1["geo-level-1"]})',
            f'{self.mock_city_2["name"]}....(GL1: {self.mock_city_2["geo-level-1"]})',
            'Аврен....(GL1: northeastern; GL2: VAR01)',
        ]
        cities = map_geo(cities)
        mapped_neigh = map_neighborhoods(cities, 'neigh.txt')
        self.assertEqual(
            self.expected_mapped_neigh, 
            mapped_neigh
        )

    def test_map_neighborhoods_neigh_map_returns_cities_mapped_to_their_neighborhoods(self):
        cities = [
            f'{self.mock_city_1["name"]}....(GL1: {self.mock_city_1["geo-level-1"]})',
            f'{self.mock_city_2["name"]}....(GL1: {self.mock_city_2["geo-level-1"]})',
            'Аврен....(GL1: northeastern; GL2: VAR01)',
        ]
        cities = map_geo(cities)
        mapped_neigh = map_neighborhoods(cities, {
            self.mock_city_1['name']: self.mock_city_1['neigh'],
            self.mock_city_2['name']: self.mock_city_2['neigh'],
        })
        self.assertEqual(
            self.expected_mapped_neigh, 
            mapped_neigh
        )

    def test_get_unmapped_polygons_returns_the_still_unmapped_polygons(self):
        polygons = 'poly-1', 'poly-2', 'poly-3'
        unmapped = get_unmapped_polygons(polygons, [0, 1])
        self.assertEqual(1, len(unmapped))
        self.assertEqual(polygons[2], unmapped[0])

    def test_get_unmapped_neighborhoods_returns_still_unmapped_neighborhoods(self):
        unmapped_polys = [
            {
                'geo': {
                    'level-1': 'sofia',
                },
                'geoJSON': 'geoJSON'
            },
            {
                'geo': {
                    'level-1': 'sofia',
                    'level-2': 'all',
                    'level-2-bg': 'Всички',
                },
                'geoJSON': 'geoJSON'
            },
            {
                'geo': {
                    'level-1': 'sofia',
                    'level-2': 'neigh-1',
                    'level-2-bg': 'Квартал-1',
                },
                'geoJSON': 'geoJSON'
            },
            {
                'geo': {
                    'level-1': 'sofia',
                    'level-2': 'neigh-2',
                    'level-2-bg': 'Квартал-2',
                },
                'geoJSON': 'geoJSON'
            }
        ]
        unmapped_neigh = get_unmapped_neighborhoods(unmapped_polys)
        self.assertEqual(
            {
                'sofia': [
                    {
                        'name': 'Квартал-1', 
                        'geoJSON': 'geoJSON'
                    },
                    {
                        'name': 'Квартал-2', 
                        'geoJSON': 'geoJSON'
                    },
                ]
            }, 
            unmapped_neigh
        )

    @patch('src.mapper.open', mock_open(read_data=mock_geo_json))
    def test_find_town_polygon_data_geo_level_1_and_2_returns_correct_polygon(self):
        data = get_raw_polygon_data('GeoJSON.json')
        poly = find_town_polygon_data(
            self.mock_geo_feature_1['properties']['geography_level_1'], 
            self.mock_geo_feature_1['properties']['geography_level_2'], 
            data
        )
        self.assertEqual(
            (
                {
                    'geo': {
                        'level-1': self.mock_geo_feature_1['properties']['geography_level_1'],
                        'level-2': self.mock_geo_feature_1['properties']['geography_level_2'],
                        'level-2-bg': self.mock_geo_feature_1['properties']['geography_level_2_bg']
                    },
                    'geoJSON': self.mock_geo_feature_1
                },
                0
            ), 
            poly
        )

    @patch('src.mapper.open', mock_open(read_data=mock_geo_json))
    def test_find_town_polygon_data_geo_level_1_only_returns_none(self):
        data = get_raw_polygon_data('GeoJSON.json')
        poly = find_town_polygon_data(
            self.mock_geo_feature_2['properties']['geography_level_1'], 
            None, 
            data
        )
        self.assertIsNone(poly)

    def test_map_areas_to_polygons_maps_areas_to_polyogns(self):
        unmapped_polys = [
            {
                'geo': {
                    'level-1': 'northeastern'   
                },
                'geoJSON': 'geoJSON'
            },
            {
                'geo': {
                    'level-1': 'northeastern',
                    'level-2': 'VAR01',
                },
                'geoJSON': 'geoJSON'
            },
        ]
        cities = ['sofia']
        places = {}
        map_areas_to_polygons(unmapped_polys, cities, places)
        self.assertEqual(
            {
                'Североизточна България': {
                    'geography': {
                        'level-1': 'northeastern'
                    }, 
                    'geoJSON': 'geoJSON', 
                    'isArea': True
                }
            }, 
            places
        )

    def test_map_cities_to_polygons_non_empty_places_maps_cities_to_polyogns(self):
        unmapped_polys = [
            {
                'geo': {
                    'level-1': 'sofia'   
                },
                'geoJSON': 'sofia_geoJSON'
            },
            {
                'geo': {
                    'level-1': 'veliko_tarnovo'   
                },
                'geoJSON': 'veliko_tarnovo_geoJSON'
            },
             {
                'geo': {
                    'level-1': 'northeastern',   
                    'level-2': 'VAR01',   
                },
                'geoJSON': 'avren_geoJSON'
            },
        ]
        cities = ['sofia', 'Велико Търново']
        places = {
            'София': {
                'geography': {
                    'level-1': 'sofia'
                }
            },
            'Велико Търново': {
                'geography': {
                    'level-1': 'veliko_tarnovo'
                }
            },
        }
        map_cities_to_polygons(unmapped_polys, cities, places)
        self.assertEqual(
            {
                'София': {
                    'geography': {
                        'level-1': 'sofia'
                    }, 
                    'geoJSON': 'sofia_geoJSON', 
                    'isCity': True
                }, 
                'Велико Търново': {
                    'geography': {
                        'level-1': 'veliko_tarnovo'
                    }, 
                    'geoJSON': 'veliko_tarnovo_geoJSON', 
                    'isCity': True
                }
            }, 
            places
        )

    def test_map_cities_to_polygons_empty_places_maps_cities_to_polyogns(self):
        unmapped_polys = [
            {
                'geo': {
                    'level-1': 'sofia'   
                },
                'geoJSON': 'sofia_geoJSON'
            },
            {
                'geo': {
                    'level-1': 'veliko_tarnovo'   
                },
                'geoJSON': 'veliko_tarnovo_geoJSON'
            },
             {
                'geo': {
                    'level-1': 'northeastern',   
                    'level-2': 'VAR01',   
                },
                'geoJSON': 'avren_geoJSON'
            },
        ]
        cities = ['sofia', 'Велико Търново']
        places = {}
        map_cities_to_polygons(unmapped_polys, cities, places)
        self.assertEqual(
            {}, 
            places
        )

    @patch('src.mapper.open', mock_open(read_data=mock_geo_json))
    def test_map_towns_to_polygons_maps_towns_to_polygons(self):
        polygons = get_raw_polygon_data('GeoJSON.json')
        places = {
            'София': {
                'geography': {
                    'level-1': 'sofia'
                }
            },
            'Аврен': {
                'geography': {
                    'level-1': 'northeastern',
                    'level-2': 'VAR01',
                }
            },
        }
        mapped_towns = map_towns_to_polygons(polygons, places)
        self.assertEqual([0], mapped_towns)

    def test_map_neighborhoods_to_polygons_maps_neighborhoods_to_polygons(self):
        unmapped_neighborhoods = {
            'sofia': [
                {'name': 'Абдовица'}
            ],
            'veliko_tarnovo': [
                {'name': 'Акация'},
                {'name': 'Асенов'},
            ],
        }
        places = {
            'София': {
                'geography': {
                    'level-1': 'sofia'
                }
            },
            'Велико Търново': {
                'geography': {
                    'level-1': 'northcentral'
                },
                'neighborhoods': [
                    'Изберете всички',
                    'Акация',
                    'Асенов'
                ]
            },
        }
        cities = map_neighborhoods_to_polygons(
            unmapped_neighborhoods,
            places
        )
        self.assertEqual(['sofia', 'Велико Търново'], cities)

    @patch('src.mapper.open', mock_open(read_data=mock_geo_json))
    def test_map_polygons_maps_places_to_polygons(self):
        places = {
            **self.expected_mapped_neigh,
            'Североизточна България': {
                'geography': {
                    'level-1': 'northeastern'
                }
            }
        }
        mapped_places = map_polygons(places, 'GeoJSON.json')
        self.assertEqual(self.expected_mapped_places, mapped_places)