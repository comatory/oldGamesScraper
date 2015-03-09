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

Everything should be working fine if you Xcode tools installed. If you are getting `CodecError` you might need to install _libjpeg_ library: either via [MacPorts](http://ethan.tira-thompson.com/Mac_OS_X_Ports.html) or [Homebrew](http://brew.sh):

	brew install libjpeg

### Linux

Make sure you have _libjpeg_ library installed to prevent `CodecError`. Uninstall Pillow/PIL if it is already on your system `pip uninstall PIL`.

yum : `yum install libjpeg-devel`

apt-get: `apt-get install libjpeg-dev`

Make sure you install Pillow again after the library is installed.

### Windows

Will work fine with provided modules (see above [Requirements](#requirements)).

## Usage

Run the script with one or more arguments. The first argument is the title magazine, the other ones are issue numbers (see below on numbering). 

The following command will download issues 2, 5 and 6 of Score magazine:

	python oldGamesScraper.py score 2 5 6

If you omit the issue numbers, script will proceed to download entire catalog of issues. For example to download all issues of Excalibur, do the following:

	python oldGamesScraper.py excalibur

If you need to see all available magazines, launch the script with `--list` argument. 

	python oldGamesScraper.py --list

## Numbering

One note on the numbering of the magazines. The numbers actually refer to indexes. For example issue [*Excalibur 20+*](http://www.oldgames.sk/mag/excalibur-20-plus/) has index number 24. _Excalibur Zero (0)_ has index number of 1.
You can count the order of the magazine you wish to download on the webpage (start from number one) to get the exact issue. For most of the magazines the index numbers should equal to actual issue numbers. The filename of PDFs should correspond to the right issue number (as stated on website). Some magazines are renamed due to illegal characters like `/` and `\`.

## Manual addition

You can add additional magazines into the `MAGAZINES` dictionary in the commented section.

## To be added

- add argument for JPEG-only download
- add ePub export
- scrape also Diskmags
