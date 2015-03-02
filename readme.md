# oldGamesScraper

Script that converts JPEGs from [oldgames.sk magazines](http://www.oldgames.sk/mags/) section into multi-paged PDFs. No copyright infringement intended.

## Requirements

The script is written in Python 2.7 and is dependent on some built-in packages (urllib2) and these packages:

- [Pillow](http://pillow.readthedocs.org/installation.html) (2.7.9)
- [PyPDF2](http://mstamy2.github.io/PyPDF2/) (1.24)
- [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/bs4/doc/) (2.7.0)

These can all be installed easily via [pip](https://pypi.python.org/pypi/pip/). Example `pip install urllib2`. Everything works well in `virtualenv` and it is actually a recommended way to run this script.

## Usage

Run script file with single argument. This argument is the title of the magazine and the script will proceed to download all issues (pagination on magazine page not yet supported). For example:

	python oldGamesScraper.py score

This will download all the issues of Score magazine. If you need to see all available magazines, launch the script with `--list` argument.

	python oldGamesScraper.py --list

You can add additional magazines into the `magazines` dictionary in the commented section.

## To be added

- download individual issues
- make script future proof (add pagination)
- add argument for JPEG-only download
- add ePub export

