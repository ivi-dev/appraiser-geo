"""
This module contains common type aliases.
"""


from typing import Iterable


Geo = dict[str, str]
Neigborhoods = Iterable[str]
PartialCity = dict[str, Geo]
City = dict[str, Geo | Neigborhoods]