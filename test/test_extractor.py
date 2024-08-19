# pylint: skip-file

import unittest
from unittest.mock import mock_open

from unittest.mock import patch

from src.extractor import extract_geo_data


class TestExtractor(unittest.TestCase):
    mock_csv = '''\
geography_level_1,geography_level_2,geography_level_2_bg
sofia,Izgrev,Изгрев
sofia,Goce Delchev,Гоце Делчев
sofia,Borovo,Борово
sofia,all,всички
veliko_tarnovo,Veliko Tarnovo Hills,Велико Търново Хилс
veliko_tarnovo,Cholakovtsi,Чолаковци
veliko_tarnovo,outskirts,Покрайнини
southwestern,BLG52,Хаджидимово
northwestern,LOV18,Ловеч
northeastern,DOB20,Крушари
northcentral,VTR04,Велико Търново
'''

    @patch('src.extractor.open', mock_open(read_data=mock_csv))
    def test_transform_geo_data_returns_cities_and_neighborhoods(self):
        cities, neighborhoods = extract_geo_data('geo.csv')
        self.assertEqual([
                'Велико Търново.....(GL1: northcentral; GL2: VTR04)',
                'Крушари.....(GL1: northeastern; GL2: DOB20)', 
                'Ловеч.....(GL1: northwestern; GL2: LOV18)', 
                'София.....(GL1: sofia)', 
                'Хаджидимово.....(GL1: southwestern; GL2: BLG52)',
            ], cities
        )
        self.assertEqual({
            'София': ['Изгрев', 'Гоце Делчев', 'Борово', '--Всички--'],
            'Велико Търново': ['Велико Търново Хилс', 'Чолаковци', 'Покрайнини']
        }, neighborhoods
        )