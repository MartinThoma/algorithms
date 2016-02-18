## Idea

Create a single HTML page from a BibTeX file.

See https://twitter.com/fortnow/status/698932411137200129


## Requirements

You have to have Python and the default Python package manager `pip` installed.

Install the requirements by `pip install -r requirements.txt`


## Usage

```bash
$ ./create_html.py --help

usage: create_html.py [-h] [-b BIBTEXFILE] [-o OUTPUTHTML]

Create a HTML file from a .bibtex file.

optional arguments:
  -h, --help            show this help message and exit
  -b BIBTEXFILE, --bibtex BIBTEXFILE
                        read bibtex file from this location (default:
                        example.bib)
  -o OUTPUTHTML, --out OUTPUTHTML
                        path where to write generated HTML code (default:
                        out.html)

```


## Output

See [out.html](https://github.com/MartinThoma/algorithms/blob/master/bib2html/out.html)


## Known Issues

* https://github.com/sciunto-org/python-bibtexparser/issues/116