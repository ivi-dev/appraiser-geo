# pylint: skip-file

import unittest

from src.translit import Transliterator


class TestTranslit(unittest.TestCase):
    def test_translit_transliterates_a_val_without_spell_correction(self):
        transliter = Transliterator(locale='bg')
        res = transliter.translit('zdravey sviat')
        self.assertEqual('здравей свиат', res)

    def test_translit_transliterates_a_val_with_spell_correction(self):
        transliter = Transliterator(locale='bg', corr_table={'здравей свиат': 'здравей свят'})
        res = transliter.translit('zdravey sviat')
        self.assertEqual('здравей свят', res)