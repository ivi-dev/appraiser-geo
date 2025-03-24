"""
This module contains common type aliases.
"""


from typing import Iterable


# A place's (city/town) geographical data,
# mainly its geography level 1 and 2
Geo = dict[str, str]

# A city's neighborhoods
Neigborhoods = Iterable[str]

# A lat/lon coordinate pair
LatLon = tuple[float, float]

# A polygon ring, either "inner" or "outer".
# Check https://stevage.github.io/geojson-spec/#section-3.1.6
# for details
PolygonRing = tuple[LatLon, ...]

# GeoJSON polygon data, consisting of one or more "rings".
# Check https://stevage.github.io/geojson-spec/#section-3.1.6
# for details
Polygons = tuple[PolygonRing, ...]

# A data structure mapping certain city/town/neighborhood
# to its polygons, as published in a GeoJSON-formatted file
RawPolygonDataItem = dict[str, Geo | Polygons]

# A data structure mapping certain cities/town/neighborhoods
# to their polygons, as published in a GeoJSON-formatted file
RawPolygonData = Iterable[RawPolygonDataItem]

# A city's neighborhoods, enriched with their
# (GeoJSON) polygons data
GeoNeigborhoods = Iterable[dict[str, str | Polygons]]

# A city/town mapped to its geography level 1 and (possibly)
# 2 info only
GeoCity = dict[str, Geo]

# A city/town mapped to its geography level 1 and (possibly)
# 2 and partitioned into neighborhoods
PartitionedCity = dict[str, Geo | Neigborhoods]

# A city/town mapped to its entire geo data - geography
# level 1 and (possibly) 2, neighborhoods and polygons.
# Here, the city/town's neighborhoods are mapped to their
# own polygon data too.
FullCity = dict[str, Geo | GeoNeigborhoods | Polygons]
