# -*- coding: utf-8 -*-

import os
import sys
import urllib2
from copy import deepcopy
from PIL import Image, ImageFile
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from bs4 import BeautifulSoup

ImageFile.LOAD_TRUNCATED_IMAGES = True

class IssueException(Exception):
	def __init__(self):
		print 'Issue number fail/not existing (use number only)'

class IssueNameException(Exception):
	def __init__(self):
		print 'Use issue names only, see `--list`'

class ArgException(Exception):
	def __init__(self):
		print 'Too many arguments'

def parser(args):
	if len(args) == 2 and not args[1].isdigit():
		return args[1].lower(), 'all'
	elif args[1].isdigit():
		raise IssueNameException

	if len(args) >= 3 and not args[1].isdigit():
		for arg in args[2:]:
			if not arg.isdigit():
				raise ArgException
		return args[1].lower(), args[2:]
	else:
		raise IssueException

the_url = 'http://www.oldgames.sk'
base_url = the_url + '/mags/'

# Add magazines + relative URLs here
MAGAZINES = {
		'score': 'score/',
		'level': 'level/',
		'amiga': 'amiga-magazin/',
		'bit': 'bit/',
		'commodore': 'commodore-amater/',
		'CGW': 'cgw/',
		'excalibur': 'excalibur/',
		'hrac': 'hrac-cz/',
		'joystick': 'joystick-sk/',
		'pocitac-aktivne': 'pocitac-aktivne/',
		'pocitacove-hry': 'pocitacove-hry/',
		'riki': 'riki/',
		'zzap64': 'zzap64/'}


def extract_magazine_page(parsed):
	if parsed[0] in MAGAZINES:
		print 'Scraping %s ...' % parsed[0].capitalize()
		return base_url + MAGAZINES[parsed[0]]
	else:
		raise IssueNameException

def extract_links_to_issue(url, parsed):
	issue_links = []
	soup = BeautifulSoup(urllib2.urlopen(url))

	for div in soup.findAll('div','mImage'):
		issue_links.append(the_url + div.a['href'])

	if parsed[1] != 'all':
		temp_issue_links = [] 
		for issue_indexes in parsed[1:]:
			for issue in issue_indexes:
				try:
					temp_issue_links.append(issue_links[int(issue) - 1])
				except IndexError:
					raise IssueException

		return temp_issue_links

	print 'Scraped %d links' % len(issue_links)
	return issue_links

def issue_renamer(issue_name):
	char1 = '\\'
	char2 = '/'
	replacement = '-'
	if char1 in issue_name:
		issue_name = issue_name.replace(char1, replacement)
		print 'inv. char (%s): renaming to %s' % (char1, issue_name)
	elif char2 in issue_name:
		issue_name = issue_name.replace(char2, replacement)
		print 'inv. char (%s): renaming to %s' % (char2, issue_name)

	return issue_name

def extract_links_to_images(issue_links):
	download_list = {}
	for index, link in enumerate(issue_links):
		print 'Scraping in queue %d/%d: %s' % (index + 1, len(issue_links), link)
		issue_soup = BeautifulSoup(urllib2.urlopen(link))
		image_list = []
		for image in issue_soup.findAll('div', 'mags_thumb_article'):
			issue_name = issue_renamer(issue_soup.findAll('h1','top')[0].text)
			image_list.append(the_url + image.a['href'])

		download_list[issue_name] = image_list
	
	return download_list

def clean_up(list_of_files, list_of_pdfs):
	num = len(list_of_files) + len(list_of_pdfs)
	for file in list_of_files:
		os.remove(file)
	for pdf in list_of_pdfs:
		os.remove(pdf)
	print 'Cleaned up %d files' % num

def convert_images(list_of_files, issue):
	list_of_pdfs = []
	for index, file in enumerate(list_of_files):
		im = Image.open(file)
		outfile = file + '.pdf'
		im.save(outfile, 'PDF')
		list_of_pdfs.append(outfile)

		print 'converting ...' + str((index + 1)) + '/' + str(len(list_of_files))

	final_pdf = PdfFileMerger()
	for pdf in list_of_pdfs:
		final_pdf.append(open(pdf, 'rb'))

	issue_name = issue + '.pdf'
	final_pdf.write(open(issue_name, 'wb'))
	final_pdf.close()
	print '--- PDF completed ---'

	clean_up(list_of_files, list_of_pdfs)

def download_images(download_list):
	for issues,image_list in download_list.items():
		print 'Preparing %s ...' % issues
		list_of_files = []
		for image in image_list:
			image_name = os.path.split(image)[1]
			list_of_files.append(image_name)
			f = open(image_name, 'wb')
			f.write(urllib2.urlopen(image).read())
			print 'Downloading image: %s' % image
			f.close()
		convert_images(list_of_files, issues)

parsed = parser(sys.argv)
url = extract_magazine_page(parsed)
issue_links = extract_links_to_issue(url, parsed)
download_list = extract_links_to_images(issue_links)
list_of_files = download_images(download_list)
