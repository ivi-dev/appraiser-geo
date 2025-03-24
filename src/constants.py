"""
This module contains common constants.
"""

# Regex
CITY_NAME_GROUP = 'city_name'
CITY_DELIM_GROUP = 'delim'
GEO_LEVEL_1_GROUP = 'gl1'
GEO_LEVEL_2_GROUP = 'gl2'
CITY_REGEX = fr'(?P<{CITY_NAME_GROUP}>.+?)'                  \
             fr'(?P<{CITY_DELIM_GROUP}>\.+?)'                \
             fr'\(GL1:\s*(?P<{GEO_LEVEL_1_GROUP}>.+?)'       \
             fr'(;\s*GL2:\s*(?P<{GEO_LEVEL_2_GROUP}>.+?))*\)'
CITY_DELIM_REGEX = r'^\s*-+\s*$'
CITY_NAME_REGEX = f'^(?P<{CITY_NAME_GROUP}>.+):$'

# Keys
GEO_KEY = 'geography'
GEO_LEVEL_1_KEY = 'level-1'
GEO_LEVEL_2_KEY = 'level-2'
NEIGHBORHOODS_KEY = 'neighborhoods'

# Misc
AREA_NAMES = {
    'northwestern': 'Северозападна България',
    'northcentral': 'Северна България',
    'northeastern': 'Североизточна България',
    'southwestern': 'Югозападна България',
    'southcentral': 'Южна България',
    'southeastern': 'Югоизточна България',
}
ALL = 'всички'
DEFAULT_ALL = 'Изберете всички'
