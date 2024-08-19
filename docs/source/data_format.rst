Data formatting
==================

Appraiser Geo expects the content of the input files it works with
to be formatted a certain way. Here are some examples of properly 
formatted content of the cummulative geo data, well as the city and 
neighborhood lists. "*GL1*" is the place's geography level 1 ID and 
"*GL2*" - the geogrphy level 2 one. The examples are truncated for 
brevity:


.. _csv-format:

*All_Geo.csv*
-------------

This file may be named whatever you choose and has to contain
comma-spearated values in three columns: the place's geography 
level 1 ID, geography level 2 ID in english and bulgarian
respectively. All populated places, including towns, cities and
their neighborhoods are expected to be here.

::

    geography_level_1,geography_level_2,geography_level_2_bg
    sofia,Izgrev,Изгрев
    sofia,Goce Delchev,Гоце Делчев
    sofia,Borovo,Борово
    sofia,Strelbishte,Стрелбище
    sofia,Pancharevo - Chereshovi gradini,Панчарево - Черешови градини
    southwestern,BLG52,Хаджидимово
    northwestern,LOV18,Ловеч
    northeastern,DOB20,Крушари
    southeastern,SLV11,Котел
    southwestern,BLG53,Якоруда
    southcentral,KRZ02,Ардино
    northeastern,VAR01,Аврен
    southcentral,KRZ15,Крумовград
    northcentral,GAB29,Севлиево
    southcentral,KRZ14,Кирково
    ...


.. _city-format:

*Cities.txt*
------------

This file may be named whatever you choose and has to contain line-separated 
populated places along with their geography level data.

::

    София..............(GL1: sofia)
    Пловдив............(GL1: plovdiv)
    Варна..............(GL1: varna)
    Бургас.............(GL1: burgas)
    Русе...............(GL1: ruse)
    Стара Загора.......(GL1: stara_zagora)
    Велико Търново.....(GL1: veliko_tarnovo)
    Благоевград........(GL1: blagoevgrad)
    Хаджидимово........(GL1: southwestern; GL2: BLG52)
    Якоруда............(GL1: southwestern; GL2: BLG53)
    Сливница...........(GL1: southwestern; GL2: SFO45)
    ...


.. _neigh-format:

*Neighborhoods.txt*
--------------------

This file may be named whatever you choose and has to contain a city's name 
delimited by at least one dash (U+002D) followed by line-separated 
names of neighborhoods located in that city.

::

    --------
    София:
    --------

    Изгрев
    Гоце Делчев
    Борово
    Стрелбище
    Панчарево - Черешови градини
    Красно село
    Детски град
    вилна зона Бункера
    вилна зона Малинова долина
    Симеоново
    Източен Парк Младост
    ...


    ---------
    Пловдив:
    ---------

    Коматево
    Беломорски
    Остромила
    Прослав
    Индустриална зона Юг
    Отдих и култура
    ...