import sys
import urllib2
from bs4 import BeautifulSoup

def parser():
	try:
		return sys.argv[1].lower()
	except IndexError:
		print 'no argument specified'


the_url = 'http://www.oldgames.sk'
base_url = the_url + '/mags/' 
magazines = {
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

issue_links = []
download_list = {} 

def parse_args(arg):
	if arg in magazines:
		print "Scraping %s magazine..." % arg.capitalize()
		return base_url + magazines[arg]
	else:
		return sys.exit('invalid magazine name')

def extract_links_to_issue(url):
	soup = BeautifulSoup(urllib2.urlopen(url))	

	for div in soup.findAll('div','mImage'):
		issue_links.append(the_url + div.a['href'])

	print 'Scraped %d links' % len(issue_links)

def extract_links_to_images(issue_links):
	for index, link in enumerate(issue_links):
		print 'Scraping issue #%d: %s' % (index + 1, link)
		issue_soup = BeautifulSoup(urllib2.urlopen(link))
		image_list = []
		for image in issue_soup.findAll('div', 'mags_thumb_article'):
			issue_name = issue_soup.findAll('h1','top')[0].text
			image_list.append(the_url + image.a['href'])

		download_list[issue_name] = image_list 

arg = parser()
extract_links_to_issue(parse_args(arg.lower()))
extract_links_to_images(issue_links)
f = open('download_list', 'w')
f.write(str(download_list))
f.close()
