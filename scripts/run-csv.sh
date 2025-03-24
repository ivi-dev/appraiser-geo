#!/bin/bash

python -m src.main --csv "./resources/geography_nomenclature_(ORIGINAL).csv" \
                   --polygons "./resources/polygons/geo-level-1.geojson" \
                              "./resources/polygons/geo-level-2.geojson" \
                   --out "./resources/Гео_Данни_Форматирани_[вход-CSV].json"