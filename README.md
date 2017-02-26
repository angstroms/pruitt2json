# pruitt2json

Let's make those PDF email dumps useful. This is a hacky set of scripts that
will make the [Pruitt email
dumps](http://www.exposedbycmd.org/Scott-Pruitt-Missing-Emails) slightly more
useful (albeit the script isn't perfect)

Go check out the [visualization](http://angstroms.github.io/pruitt2json/) to get
a sense of the data.

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


## Data Format

Each one of the `.json` files created are of the format,

```
[
    {
        'to': ['raw@email', ('Name', 'name@email')],
        'from': ['raw@email', ('Name', 'name@email')],
        'cc': ['raw@email', ('Name', 'name@email')],
        'subject': "Subject",
        'date': "Jan 1 1971",
        'attachments': ['file1.doc', 'file2.doc'],
        'body': [
            (indendation level, "text at this indentation"),
            (indentation level, "text at this indentation")
        ]
    },
    ...
]
```

The indentation level was kept in the body field to aid with quoted text from
previous emails.

Emails can be listed either as a raw email or as a tuple with the persons
provided name.  The counts of which fields are used for `Produce-4000.xml`
is:

```
Counter({'attachments': 229,
         'body': 2256,
         'cc': 639,
         'date': 2249,
         'from': 2255,
         'replyto': 521,
         'subject': 2250,
         'to': 2242})
```

## Coverage

This was a quick evening of hacking and as such the code isn't perfect. While we
do get most emails and we parse them mostly correctly, there are some errors.
One of the big assumptions we make is that every email block in the pdfs starts
with a `From:` field. For the most part this is true.

```
XML to JSON: Produce-1600-2541-Redacted.xml
        Expected number of emails: 707
        Extracted 677 emails
XML to JSON: Produce-2000.xml
        Expected number of emails: 226
        Extracted 226 emails
XML to JSON: Produce-3000.xml
        Expected number of emails: 696
        Extracted 697 emails
XML to JSON: Produce-4000.xml
        Expected number of emails: 2387
        Extracted 2256 emails
XML to JSON: Produce-5000.xml
        Expected number of emails: 141
        Extracted 123 emails
XML to JSON: Produce-6000.xml
        Expected number of emails: 176
        Extracted 137 emails
XML to JSON: Produce-Box-1-Redacted.xml
        Expected number of emails: 574
        Extracted 579 emails
XML to JSON: Produce-Box-5-Redacted.xml
        Expected number of emails: 690
        Extracted 651 emails
XML to JSON: Produce-Box-5.xml
        Expected number of emails: 690
        Extracted 651 emails
XML to JSON: Produce-Box-6.xml
        Expected number of emails: 0
        Extracted 0 emails
```

## TODO

- Get better coverage and better json qualit
- Be able to get rich media from the emails
