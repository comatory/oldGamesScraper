from nose.tools import *
from bs4 import BeautifulSoup
# package modules
from start import parse_args

def test_parse_args(): 
	base_html = 'http://www.oldgames.sk/mags/'
	magazines = {'score': 'score/'}
	assert_equal(parse_args('score'), 'http://www.oldgames.sk/mags/score/')

