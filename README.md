![Deploy](https://github.com/ivi-dev/appraiser-geo/actions/workflows/deploy.yml/badge.svg)


Appraiser Geo is a program that reads the contents of user-specified files containing populated places in Bulgaria and produces their structured textual presentation according to the [Appraiser's Geo classification](https://ivi-dev.github.io/appraiser-geo/geo_classification.html).

# Example usage

Appraiser Geo can work with either a raw CSV file with all geo data combined or a set of files with pre-formatted city and neighborhood data. Choose the option that suits your case best.

Following are examples of the two ways to pass data into the program. The end result in any case will be the same.

**Option #1**: Passing separate TEXT files:

```
appraiser_geo --cities "cities.txt" --neighborhoods "neighborhoods.txt" --out "output.json"
```

Assuming the content of `cities.txt` is:

```
Благоевград........(GL1: blagoevgrad)
Хаджидимово........(GL1: southwestern; GL2: BLG52)
Якоруда............(GL1: southwestern; GL2: BLG53)
```

And the content of `neighborhoods.txt` is:

```
-------------
Благоевград:
-------------

Струмско
Ален Мак
Еленово
```

**Option #2**: Passing a single CSV file:

```
appraiser_geo --csv "geo.csv" --out "output.json"
```

Assuming the content of the CSV file is:

```
geography_level_1,geography_level_2,geography_level_2_bg
blagoevgrad,Strumsko,Струмско
blagoevgrad,Alen Mak,Ален Мак
blagoevgrad,Elenovo,Еленово
southwestern,BLG52,Хаджидимово
outhwestern,BLG53,Якоруда
```

The result of both options will be:

```
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
```


# Installation instructions

Download a distribution archive from the "Releases" section on the app's GitHub repo page, matching your operating system. Then extract the downloaded archive onto your machine, at a file system location of your choice. Inside of the extracted directory you'll find the app's executable file. Unlike Mac and Linux, on Windows, the file will have a `.exe` extension. Run that file from the command line, passing the required options, to start the program.

To get helpful info about the program's available command-line options and more, run it with the `-h` option, e.g. `appraiser-geo -h`.

# Technical documentation
You will find the app's technical documentation, detailing its API, terms used as well as examples [here](https://ivi-dev.github.io/appraiser-geo/).