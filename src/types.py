"""
This module contains common type aliases.
"""


from typing import Iterable


# A place's (city/town) geographical data, 
# mainly its geography level 1 and 2
Geo = dict[str, str]

# A city's neighborhoods
Neigborhoods = Iterable[str]

# GeoJSON polygon data
Polygons = tuple[tuple[float, float], ...]

# A data structure mapping certain cities/town/neighborhoods
# to their GeoJSON polygons
RawPolygons = Iterable[dict[str, Geo | Polygons]]

# A city's neighborhoods, enriched with their 
# (GeoJSON) polygons data
GeoNeigborhoods = Iterable[dict[str, Polygons]]

# A city/town mapped to its geography level 1 and (possibly) 
# 2 info only
PartialCity = dict[str, Geo]

# A city/town mapped to its geography level 1 and (possibly) 
# 2 and neighborhoods
City = dict[str, Geo | Neigborhoods]

# A city/town mapped to its entire geo data - geography 
# level 1 and (possibly) 2, neighborhoods and polygons.
# Here, the city/town's neighborhoods are mapped to their 
# own polygon data too.
GeoCity = dict[str, Geo | GeoNeigborhoods | Polygons]
