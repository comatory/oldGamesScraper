# -*- coding: utf-8 -*-
from nose.tools import *
from oldGamesScraper import parser, IssueException, IssueNameException, ArgException, extract_magazine_page, extract_links_to_issue, issue_renamer, extract_links_to_images
from test_data import test_data

URL = 'http://www.oldgames.sk/mags/score/'
 
def test_parser_pass():
	sys_argv_test = ['test.py', 'Excalibur','1' ]
	assert_equal(parser(sys_argv_test), ('excalibur',['1']))

def test_parser_fail():
	sys_argv_test = ['test.py', 'Level', 'Excalibur']
	assert_raises(ArgException, parser, sys_argv_test)

def test_parser_without_issue():
	sys_argv_test = ['test.py', 'Score']
	assert_equal(parser(sys_argv_test), ('score','all'))

def test_parser_without_issue_fail():
	sys_argv_test = ['test.py', '5']
	assert_raises(IssueNameException, parser, sys_argv_test)

def test_parser_with_extra_arg():
	sys_argv_test = ['test.py', 'Score', '6', '8', '15']
	assert_equal(parser(sys_argv_test), ('score', ['6', '8', '15']))

def test_extract_magazine_page():
	parsed = ('score','all')
	assert_equal(extract_magazine_page(parsed), URL)

def test_extract_magazine_page_fail():
	parsed = ('pcgamer','all')
	assert_raises(IssueNameException, extract_magazine_page, parsed)

def test_extract_all_links_to_issue():
	parsed = ('score','all')
	issue_links = extract_links_to_issue(URL, parsed)
	# as of date Mar-7-2015 = 39 issues of Score
	assert_equal(len(issue_links), 39)

def test_extract_single_link():
	parsed = ('score', '5')
	issue_links = extract_links_to_issue(URL, parsed)
	assert_equal(len(issue_links), 1)

def test_extract_multiple_links():
	parsed = ('score', '5', '8', '10', '22')
	issue_links = extract_links_to_issue(URL, parsed)
	assert_equal(len(issue_links), 4)

def test_issue_renamer():
	assert_equal(issue_renamer('Score 2/96'), 'Score 2-96')
	assert_equal(issue_renamer('Testmag 2\\96'), 'Testmag 2-96')

def test_extract_image_links():
	issue_links = ['http://www.oldgames.sk/mag/score-2/',
				 'http://www.oldgames.sk/mag/score-5/',
				  'http://www.oldgames.sk/mag/score-6/']
	saved_data = test_data()
	assert_equal(extract_links_to_images(issue_links), saved_data) 

