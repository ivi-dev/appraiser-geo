"""
Test the app's main module.
"""

import unittest
from unittest.mock import call, mock_open, patch

from src.main import map_geo, map_neighborhoods, write_cities_json


class TestMain(unittest.TestCase):
    mock_neighborhoods = '''
    --------------

    Стара Загора:

    --------------

    Квартал СЗ 1
    Квартал СЗ 2
    Квартал СЗ 3



    ----------------

    Велико Търново:

    ----------------

    Квартал ВТ 1
    Квартал ВТ 2
    Квартал ВТ 3
                         
    

    --------------

    Благоевград:

    --------------

    Квартал БГ 1
    Квартал БГ 2
    Квартал БГ 3
    '''

    neighborhood_mapped_cities = {
        'Стара Загора': {
            'geography': {
                'level-1': 'stara_zagora'
            }, 
            'neighborhoods': [
                'Квартал СЗ 1',
                'Квартал СЗ 2',
                'Квартал СЗ 3'
            ]
        },
        'Велико Търново': {
            'geography': {
                'level-1': 'veliko_tarnovo',
                'level-2': 'VTR04'
            }, 
            'neighborhoods': [
                'Квартал ВТ 1',
                'Квартал ВТ 2',
                'Квартал ВТ 3'
            ]
        },
        'Благоевград': {
            'geography': {
                'level-1': 'blagoevgrad'
            }, 
            'neighborhoods': [
                'Квартал БГ 1',
                'Квартал БГ 2',
                'Квартал БГ 3'
            ]
        }
    }

    def test_map_geo_maps_cities_to_their_geo_levels(self):
        cities = [
            'non-city',
            'Благоевград........(GL1: blagoevgrad)',
            'Хаджидимово........(GL1: southwestern; GL2: BLG52)',
            'Якоруда............(GL1: southwestern; GL2: BLG53)',
        ]
        mapped = map_geo(cities)
        self.assertEqual({
            'Благоевград': {'geography': {'level-1': 'blagoevgrad'}},
            'Хаджидимово': {'geography': {'level-1': 'southwestern', 'level-2': 'BLG52'}},
            'Якоруда': {'geography': {'level-1': 'southwestern', 'level-2': 'BLG53'}},
        }, mapped)

    @patch('src.main.open', mock_open(read_data=mock_neighborhoods))
    def test_map_neighborhoods_filepath_maps_cities_to_neighborhoods(self):
        cities = {
            'Благоевград': {'geography': {'level-1': 'blagoevgrad'}},
            'Велико Търново': {'geography': { 'level-1': 'veliko_tarnovo', 'level-2': 'VTR04' }},
            'Стара Загора': {'geography': {'level-1': 'stara_zagora'}}
        }
        mapped = map_neighborhoods(cities, 'neighborhoods.txt')
        self.assertEqual(self.neighborhood_mapped_cities, mapped)

    def test_map_neighborhoods_cities_map_maps_cities_to_neighborhoods(self):
        cities = {
            'Благоевград': {'geography': {'level-1': 'blagoevgrad'}},
            'Велико Търново': {'geography': { 'level-1': 'veliko_tarnovo', 'level-2': 'VTR04' }},
            'Стара Загора': {'geography': {'level-1': 'stara_zagora'}}
        }
        neighborhoods = {
            'Благоевград': [
                'Квартал БГ 1',
                'Квартал БГ 2',
                'Квартал БГ 3'
            ],
            'Стара Загора': [
                'Квартал СЗ 1',
                'Квартал СЗ 2',
                'Квартал СЗ 3'
            ],
            'Велико Търново': [
                'Квартал ВТ 1',
                'Квартал ВТ 2',
                'Квартал ВТ 3'
            ],
        }
        mapped = map_neighborhoods(cities, neighborhoods)
        self.assertEqual(self.neighborhood_mapped_cities, mapped)

    @patch('src.main.open')
    def test_write_cities_writes_cities_to_file(self, open):
        write_cities_json(self.neighborhood_mapped_cities, 'cities.txt')
        self.assertEqual(call('cities.txt', 'wt', encoding='utf8'), open.mock_calls[0])
        self.assertEqual(call().__enter__(), open.mock_calls[1])
        self.assertEqual(call().__enter__().write(
            '''\
{
    "Стара Загора": {
        "geography": {
            "level-1": "stara_zagora"
        },
        "neighborhoods": [
            "Квартал СЗ 1",
            "Квартал СЗ 2",
            "Квартал СЗ 3"
        ]
    },
    "Велико Търново": {
        "geography": {
            "level-1": "veliko_tarnovo",
            "level-2": "VTR04"
        },
        "neighborhoods": [
            "Квартал ВТ 1",
            "Квартал ВТ 2",
            "Квартал ВТ 3"
        ]
    },
    "Благоевград": {
        "geography": {
            "level-1": "blagoevgrad"
        },
        "neighborhoods": [
            "Квартал БГ 1",
            "Квартал БГ 2",
            "Квартал БГ 3"
        ]
    }
}'''
        ), open.mock_calls[2])
        self.assertEqual(call().__exit__(None, None, None), open.mock_calls[3])