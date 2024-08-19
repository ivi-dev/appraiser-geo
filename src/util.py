"""
This module contains general helping utilities.
"""

from typing import Iterable, Mapping

from src.constants import NEIGHBORHOODS_KEY
from src.types import City


def print_dict(dict: Mapping[any, any]) -> None:
    """
    Print the specified dictionary to the standard output.

    Example:

    >>> print_dict({'a': 1, 'b': 2, 'c': {'d': 3}})
    >>> 'a': 1
    >>> 'b': 2
    >>> 'c': {'d': 3}
    """

    for key in dict:
        print(f'{key}: {dict[key]}')


def read_sorted(path: str) -> Iterable[str]:
    """
    Return the lines of the file at ``path`` in 
    ascending alphabetical order.

    Example:

    We have a *file.txt* with the following content::
    
        c
        b
        a

    Sort-reading it produces:

    >>> read_sorted('file.txt')
    >>> ['a', 'b', 'c']
    """

    with open(path, 'rt', encoding='utf8') as file:
        return sorted(file.readlines())


def sort_neighborhoods(cities: Mapping[str, City]) -> Mapping[str, City]:
    """
    Sort the provided ``cities``' neighborhoods in alphabetical 
    ascending order.
    """

    for _, info in cities.items():
        if NEIGHBORHOODS_KEY in info:
            info[NEIGHBORHOODS_KEY] = sorted(info[NEIGHBORHOODS_KEY])
    return cities