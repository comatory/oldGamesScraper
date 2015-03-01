import sys
import urllib2
from bs4 import BeautifulSoup

def parser():
	try:
		return sys.argv[1].lower()
	except IndexError:
		print 'no argument specified'


base_html = 'http://www.oldgames.sk/mags/'
magazines = {
		'score': 'score/',
		'level': 'level/'} 
issue_links = []

def parse_args(arg):
	arg.lower()
	if arg in magazines:
		print "Scraping %s magazine..." % arg.capitalize()
		return base_html + magazines[arg]
	else:
		return sys.exit('invalid magazine name')

def extract_links_to_issue(url):
	soup = BeautifulSoup(urllib2.urlopen(url))	

	for div in soup.findAll('div','mImage'):
		issue_links.append(base_html + div.a['href'])

arg = parser()
extract_links_to_issue(parse_args(arg))

print issue_links

