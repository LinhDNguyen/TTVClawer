#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
from lib.epubgen2 import EpubGenerator
from bs4 import BeautifulSoup
import codecs

def get_html_page(url):
	result = u''
	if sys.version_info.major > 2:
		# python3
		import urllib.request
		fp = urllib.request.urlopen(url)
		mybytes = fp.read()
		result = mybytes.decode("utf8")
		fp.close()
	else:
		# python2
		import urllib
		fp = urllib.urlopen(url)
		mybytes = fp.read()
		try:
			result = mybytes.decode("utf8", errors="replace")
		except Exception as ex:
			print("ERR: %s" % (traceback.format_exc()))
		fp.close()

	return result

def write_file(path, content):
	fp = codecs.open(path, "w", "utf-8")
	fp.write(content)
	fp.close()


class TTVChapter(object):
	"""Chapter class of TTV"""
	def __init__(self, url):
		super(TTVChapter, self).__init__()
		self.url = url
		self.title = u'__UNKNOWN__'
		self.content = u'__UNKNOWN__'
		self.number = -1

		self.parse()

	def parse(self):
		pass

class TTVClawer2(object):
	"""New version of TTV Clawer, now we claw truyen.tangthuvien.vn"""
	def __init__(self, url, title, author, output='./'):
		super(TTVClawer2, self).__init__()
		self.url = url
		self.title = title
		self.author = author
		self.output = output

		self._chapter_list = []

	def _getChapterList(self):
		max_page_number = -1

		html = get_html_page(self.url)
		root_obj = BeautifulSoup(html, 'html.parser')

		### Get story id
		id_obj = root_obj.find('input', attrs={'id':'story_id_hidden', 'name':'story_id'})
		story_id = id_obj['value']

		### Get list of chapter
		# url: https://truyen.tangthuvien.vn/doc-truyen/page/17299?page=0&limit=10000&web=1
		url = "https://truyen.tangthuvien.vn/doc-truyen/page/%s?page=0&limit=10000&web=1" % (story_id)
		print("Url to get list chapter: %s" % url)
		html = get_html_page(url)

		### Parse chapter list
		root_obj = BeautifulSoup(html, 'html.parser')
		ul_obj = root_obj.find('ul', attrs={'class':'cf'})
		if not ul_obj:
			raise Exception("Can't find ul element contains list chapter")
		for li_obj in ul_obj.find_all('li'):
			a_obj = li_obj.find('a')

			if not 'title' in a_obj.attrs.keys():
				continue
			link = a_obj['href']
			title = a_obj['title']

			self._chapter_list.append({'title': title, 'link': link})

	def _getChapterContent(self, title, url):
		result = u''

		html = get_html_page(url)
		root_obj = BeautifulSoup(html, 'html.parser')

		content_obj = root_obj.find('div', attrs={'class': re.compile(r'.*box-chap.*')})
		if not content_obj:
			raise Exception("Can't get content of chapter %s" % (url))
		result = u"<h5>%s</h5><br \\>" % (title)
		try:
			result += "<p>" + content_obj.prettify() + "</p>"
		except:
			print("ERR: can't get content of chapter: %s <> %s" % (title, url))

		return result

	def start(self):
		self._getChapterList()

		epub = EpubGenerator(self.title, self.author)
		abs_path = os.path.abspath(self.output)

		for chapter in self._chapter_list:
			content = self._getChapterContent(chapter['title'], chapter['link'])

			# replace new line
			content2 = "<br />".join(content.split("\n"))

			epub.add_chapter(chapter['title'], '', content2)
			print("Chapter: %s, %d bytes" % (chapter['title'], len(content2)))

		epub.write_book(abs_path, self.title)
		print("%d chapter created" % (len(self._chapter_list)))
