# -*- coding: utf-8 -*-

import os
import sys
import urllib2
import pdb
from copy import deepcopy
from PIL import Image, ImageFile
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from bs4 import BeautifulSoup

ImageFile.LOAD_TRUNCATED_IMAGES = True

# EXCEPTION errors

class IssueException(Exception):
	def __init__(self):
		print '\nIssue number fail/not existing (use number only)'
                exit(0)

class IssueNameException(Exception):
	def __init__(self):
		print '\nUse issue names only, see `--list`'
                exit(0)

class ArgException(Exception):
	def __init__(self):
		print '\nToo many arguments'
                exit(0)

# Command-line parser

def parser(args):

	if args[1] == '--list':
		print '\n', 'Available parameters:'
		for mag in sorted(MAGAZINES.keys()):
			print mag
		sys.exit(0)

	# enable DL for all issues
	if len(args) == 2 and not args[1].isdigit():
		return args[1].lower(), 'all'
	elif args[1].isdigit():
		raise IssueNameException

	# all args following issue name (string) must be ints
	if len(args) >= 3 and not args[1].isdigit():
		for arg in args[2:]:
			if not arg.isdigit():
				raise ArgException
		return args[1].lower(), args[2:]
	else:
		raise IssueException

the_url = 'http://www.oldgames.sk'
base_url = the_url + '/mags/' # hub page for all magazines & diskmags

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
		'zzap64': 'zzap64/',
                # diskmags:
                'bonus': 'bonus/',
                'guru': 'guru/',
                'klan': 'klan/',
                'narsil': 'narsil/',
                'pareniste': 'pareniste/',
                'pcengine': 'pcengine/',
                'slanina': 'slanina/'
                }


# returns URL of magazine that was passed as arg

def extract_magazine_page(parsed):
	if parsed[0] in MAGAZINES:
		print 'Scraping %s ...' % parsed[0].capitalize()
		return base_url + MAGAZINES[parsed[0]]
	else:
		raise IssueNameException


# gets links to individual issues

def extract_links_to_issue(url, parsed):
	issue_links = []
        page_urls = []
	soup = BeautifulSoup(urllib2.urlopen(url), "html.parser")

        # get URLs if paginated
        page_count = len(soup.findAll('table', 'paging_box')[0].findAll('span', 'paging_PageInactive'))
        page_count += 1

        # set up paginated issue pages
        for page in range(0, page_count):
            page_urls.append(url + 'pages/' + str(page))

	# gets URLs of issues to list
        for page_url in page_urls:
            soup = BeautifulSoup(urllib2.urlopen(page_url), "html.parser")
            for div in soup.findAll('div','mImage'):
                    issue_links.append(the_url + div.a['href'])

	# only when DLing all issues
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


# Avoiding illegal chars to not create folders

def issue_renamer(issue_name):
	char1 = '\\'
	char2 = '/'
	replacement = '-'
	old_name = deepcopy(issue_name)
	if char1 in issue_name:
		issue_name = issue_name.replace(char1, replacement)
	elif char2 in issue_name:
		issue_name = issue_name.replace(char2, replacement)
	
	# fix `old_name` error, get rid of multiple displays
	print 'Renamed %s to %s (inv. char.)' % (old_name, issue_name)
	return issue_name


# Check if magazine page has more pages

def paginate_check(url):
	paginate_soup = BeautifulSoup(urllib2.urlopen(url), "html.parser")
	# tag for `next page` button
	paginate = paginate_soup.findAll('span', 'paging_PageInactive')
	issue_links= []

	if paginate:
		print 'Pagination detected'
		for page in paginate:
			try:
				issue_links.append(the_url + page.a['href'])
			except AttributeError:
				pass
		
	# delete duplicate links
	clean_links = []
	for link in issue_links:
		if link in clean_links:
			pass
		else:
			clean_links.append(link)

		if link == None:
			clean_links.remove(link)

	return clean_links 


# Collect all links to JPEGs, assign to issue number

def extract_links_to_images(issue_links):
	download_list = {} # will be passed for converting
	more_pages = [] # for pagination only

	# check pagination
	for link in issue_links:
		print 'checking pagination in ', link
		more_pages.append(paginate_check(link))

	for link_set in more_pages:
		for link in link_set:
			issue_links.append(link)

	# process all links, assign them to `download_list` dict
	for index, link in enumerate(issue_links):
		print 'Scraping in queue %d/%d: %s' % (index + 1, len(issue_links), link)
		issue_soup = BeautifulSoup(urllib2.urlopen(link))
		image_list = [] # list w/ full-res image links
		for image in issue_soup.findAll('div', 'mags_thumb_article'):
			issue_name = issue_renamer(issue_soup.findAll('h1','top')[0].text)
			image_list.append(the_url + image.a['href'])

		# updates existing issue number (key), it's a check for paginated URLs
		if issue_name in download_list.keys():
			download_list[issue_name] += image_list # append new URLs to existing ones
			# update with collections.defaultdict
			# http://stackoverflow.com/questions/10664856/make-dictionary-with-duplicate-keys-in-python
		else:
			download_list[issue_name] = image_list

	return download_list


# Deletes all JPEGs and single-paged PDFs

def clean_up(list_of_files, list_of_pdfs):
	num = len(list_of_files) + len(list_of_pdfs)
	for file in list_of_files:
		try:
			os.remove(file)
		except OSError:
			pass
	for pdf in list_of_pdfs:
		try:
			os.remove(pdf)
		except OSError:
			pass
	print 'Cleaned up %d files' % num


# Convert existing JPEGs to PDFs
# then combine into multi-paged PDF

def convert_images(list_of_files, issue):
	list_of_pdfs = [] # records files jpeg -> PDF

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


# Write/DL JPEGs to disk

def download_images(download_list):
	for issues,image_list in download_list.items():
		# fix number, add real number from h1
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
