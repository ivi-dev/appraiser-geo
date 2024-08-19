"""
This module contains utilities for transliterating
values into a certain locale.
"""

from typing import Mapping
from transliterate import translit


class Transliterator:
    """
    A class for objects that transliterate values
    into a certain locale with the option to correct 
    common spelling errors.
    """

    def __init__(self, locale: str, corr_table: Mapping[str, str] | None = None) -> None:
        """
        Initialize a new instance with the specified locale
        and spell correction table.

        The correction table should contain common spelling 
        errors and has to be keyed on the lowercased incorrect 
        spelling, e.g.::
         
            {
                ...,
                'incorrect': 'Correct'
                ...,
            }
        """

        self.locale = locale
        self.corr_table = corr_table

    def translit(self, name: str) -> str:
        """
        Transliterate the specified `name` into `locale`,
        also performing a spell correction by default, 
        as per `correct`.
        
        This method uses the 
        `transliterate <https://pypi.org/project/transliterate/>`_
        library for doing the transliteration.
        """

        val = translit(name, self.locale)
        return self._correct_spelling(val) if self.corr_table else val

    def _correct_spelling(self, val: str) -> str:
        """
        Correct the spelling of `val` according to this  
        instance's spell correction table.
        """

        val_ = val.lower()
        return self.corr_table[val_] if val_ in self.corr_table else val
