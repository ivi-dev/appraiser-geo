.. Appraiser Geo documentation master file, created by
   sphinx-quickstart on Wed Jul 24 16:14:34 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Appraiser Geo documentation
===========================

Appraiser Geo is a program that reads the contents of user-specified 
files containing populated places in Bulgaria and produces their structured 
textual presentation according to the :doc:`geo_classification`.

Example usage
--------------

Appraiser Geo can work with either a raw CSV file with all geo data combined
or a set of files with pre-formatted city and neighborhood data. Choose the 
option that suits your case best.

Following are examples of the two ways to pass data into the program. The end 
result in any case will be the same.

**Option #1**: Passing separate TEXT files::

   appraiser_geo --cities "cities.txt" --neighborhoods "neighborhoods.txt" --out "output.json"

Assuming content of *'cities.txt'*::

   Благоевград........(GL1: blagoevgrad)
   Хаджидимово........(GL1: southwestern; GL2: BLG52)
   Якоруда............(GL1: southwestern; GL2: BLG53)

And the content of *'neighborhoods.txt'*::

   -------------
   Благоевград:
   -------------

   Струмско
   Ален Мак
   Еленово

**Scenario #2**: Passing A CSV file::

   appraiser_geo --csv "geo.csv" --out "output.json"

If we assume the content of the CSV file to be::

   geography_level_1,geography_level_2,geography_level_2_bg
   blagoevgrad,Strumsko,Струмско
   blagoevgrad,Alen Mak,Ален Мак
   blagoevgrad,Elenovo,Еленово
   southwestern,BLG52,Хаджидимово
   outhwestern,BLG53,Якоруда

The result of both options will be::

   {
      "Благоевград": {
         "geography": {
               "level-1": "blagoevgrad"
         },
         "neighborhoods": [
               "Струмско",
               "Ален Мак",
               "Еленово"
         ]
      },
      "Хаджидимово": {
         "geography": {
               "level-1": "southwestern",
               "level-2": "BLG52"
         }
      },
      "Якоруда": {
         "geography": {
               "level-1": "southwestern",
               "level-2": "BLG53"
         }
      }
   }


Table of contents:
------------------

.. toctree::
   :maxdepth: 2

   geo_classification
   data_format
   modules