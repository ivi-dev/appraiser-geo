Appraiser's geographic classification
======================================

The Appraiser's geographic classification assigns IDs to populated places
at two levels.

*Geography level 1* identifies either a large city or an entire geographic 
region in the country, like Sofia, Plovdiv, Varna, the country's entire 
northern, southern regions, etc.

*Geography level 2* identifies a smaller populated place, like a town, or a
neighborhood in a large city, like Hadzhidimovo, Yakoruda, Svoboda, 
Nadezhda, etc.


Examples
---------

Every populated place in the classification is identified by its geography
level 1 and 2 (if applicable) IDs in sequence. For example, to point to the 
Nadezhda neighborhood (geography level 2 ID - *"Надежда"*) in the capital 
city of Sofia (geography level 1 ID - *"sofia"*) you'd have to use::

    sofia -> Надежда

Smaller towns according to the Appraiser's classification do not have 
neighborhoods in them. You can only point to the town itself. To do that
you'd have to start with the town's containing region's geography level 1 ID,
and then specifiy the town's geogrpahy level 2 ID. For example, to
point to the town of Hadzhidimovo (geography level 2 ID - *"Хаджидимово"*) 
in the southwestern region (geography level 1 ID - *"southwestern"*) of the 
country, you'd have to use::
    
    southwestern -> Хаджидимово


Getting the latest geo data
----------------------------

To get the latest city and neighborhood lists, contact Appraiser.


Formatting input geo data
---------------------------

Check :doc:`data_format` to find out how you should format the data that you feed the 
Appraiser Geo program properly in order to get correct output.