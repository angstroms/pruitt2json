# pruitt2json

Let's make those PDF email dumps useful. This is a hacky set of scripts that
will make the [Pruitt email
dumps](http://www.exposedbycmd.org/Scott-Pruitt-Missing-Emails) slightly more
useful (albeit the script isn't perfect)

## Install

In order to run you must have `wget`, `poppler-utils` and `python3` with pip
installed.  In debian based systems that's as easy as,
```
$ sudo apt install wget poppler-utils python3 python3-pip
```

Then install the required python packages for this project with
```
$ pip3 install -r requirements.txt
```


## Run

```
$ ./pruitt2json  # win
```

This script will automatically:

- Download the pdf dump files (the 10 currently availible as of Feb 25, '17)
- Convert the PDFs to XML
- Convert the XML into nice JSON dumps (located in the [json/](json/) directory


## TODO

- Get better coverage and better json qualit
- Be able to get rich media from the emails
