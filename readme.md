# oldGamesScraper

Script that converts JPEGs from [oldgames.sk magazines](http://www.oldgames.sk/mags/) section into multi-paged PDFs. No copyright infringement intended.

## Requirements

The script is written in Python 2.7 and is dependent on some built-in packages (urllib2) and these packages:

- [Pillow](http://pillow.readthedocs.org/installation.html) (2.7.9)
- [PyPDF2](http://mstamy2.github.io/PyPDF2/) (1.24)
- [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/bs4/doc/) (2.7.0)

These can all be installed easily via [pip](https://pypi.python.org/pypi/pip/) like this:  

	pip install Pillow PyPDF2 beautifulsoup4

Everything works well in `virtualenv` and it is actually a recommended way to run this script.

### OS X

Everything should be working fine if you Xcode tools installed. If you are getting `IOError` you might need to install _libjpeg_ library: either via [MacPorts](http://ethan.tira-thompson.com/Mac_OS_X_Ports.html) or [Homebrew](http://brew.sh):

	brew install libjpeg

### Linux

Make sure you have _libjpeg_ library installed to prevent `IOError`. Uninstall Pillow/PIL if it is already on your system `pip uninstall PIL`.

yum : `yum install libjpeg-devel`

apt-get: `apt-get install libjpeg-dev`

Make sure you install Pillow again after the library is installed.

### Windows

Will work fine with provided modules (see above [Requirements](#requirements)).

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
- scrape also diskmags
