#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
from lib.epubgen2 import EpubGenerator
from bs4 import BeautifulSoup
import codecs
import pycurl
import certifi
from StringIO import StringIO
import codecs
import bs4

def get_html_page(url, use_curl=False):
	result = u''
	if use_curl:
		buffer = StringIO()
		c = pycurl.Curl()
		c.setopt(c.URL, url)
		c.setopt(c.WRITEDATA, buffer)
		c.setopt(c.CAINFO, certifi.where())
		c.setopt(c.USERAGENT, 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36')
		c.perform()
		c.close()

		body = buffer.getvalue()

		return body.decode('utf-8')
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
		print("URL: %s" % (url))
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
	def __init__(self, url, title, author, output='./', start=0, end=-1):
		super(TTVClawer2, self).__init__()
		self.url = url
		self.title = title
		self.author = author
		self.output = output
		self.begin = start
		self.end = end

		print("URL %s\ntitle %s\nauthor %s\noutput %s\nbegin %d\nend %d" % (self.url, self.title, self.author, self.output, self.begin, self.end))

		self._chapter_list = []

	def _getChapterList(self):
		max_page_number = -1

		html = get_html_page(self.url)
		root_obj = BeautifulSoup(html, 'html.parser')

		### Get story id
		id_obj = root_obj.find('input', attrs={'id':'story_id_hidden', 'name':'story_id'})
		story_id = id_obj['value']
		print("Story ID: %s" % story_id)

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
			arr = re.findall(r'(\d+)', title, re.I)
			if arr:
				ch = int(arr[0])
				if ch < self.begin:
					print("Ignore chappter %d" % (ch))
					continue
				if (self.end > 0) and (ch > self.end):
					print("Ignore chappter %d" % (ch))
					continue

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

class TruyenCVClawer(object):
	def __init__(self, url, title, author, output='./', start=0, end=-1):
		super(TruyenCVClawer, self).__init__()
		self.url = url
		self.title = title
		self.author = author
		self.output = output
		self.begin = start
		self.end = end

		print("URL %s\ntitle %s\nauthor %s\noutput %s\nbegin %d\nend %d" % (self.url, self.title, self.author, self.output, self.begin, self.end))

		self._chapter_list = []

	def start(self):
		self._getChapterList()

		epub = EpubGenerator(self.title, self.author)
		abs_path = os.path.abspath(self.output)

		# TruyenCV shows chappter lists decending. --> reverse 
		self._chapter_list.reverse()

		for chapter in self._chapter_list:
			content = self._getChapterContent(chapter['title'], chapter['link'])

			# replace new line
			content2 = "<br />".join(content.split("\n"))

			epub.add_chapter(chapter['title'], '', content2)
			print("Chapter: %s, %d bytes" % (chapter['title'], len(content2)))

		epub.write_book(abs_path, self.title)
		print("%d chapter created" % (len(self._chapter_list)))

	def _getChapterList(self):
		import urllib
		max_page_number = -1
		story_id = ''
		story_type = ''

		# Get story ID
		html = get_html_page(self.url, True)
		root_obj = BeautifulSoup(html, 'html.parser')
		id_obj = root_obj.find('a', attrs={'aria-controls':'truyencv-detail-chap'}, string='Danh sách chương')
		s = id_obj.attrs['onclick']
		# print(s) # showChapter(11259,1,1,'muc than ky')
		arr = re.findall(r'(\d+)', s, re.I)
		story_id = arr[0]
		arr = re.findall(r'\'([\w\s]+)\'', s, re.I)
		story_type = arr[0]
		print("Story ID: %s, type: %s" % (story_id, story_type))

		### Get list of chapter
		buffer = StringIO()
		c = pycurl.Curl()
		c.setopt(c.URL, 'https://truyencv.com/index.php')
		c.setopt(c.WRITEDATA, buffer)
		c.setopt(c.CAINFO, certifi.where())
		c.setopt(c.USERAGENT, 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36')
		post_data = {'showChapter':'1', 'media_id':story_id, 'number':'1', 'page':'1000', 'type': story_type}
		postfields = urllib.urlencode(post_data)
		print("post data: %s" %  (postfields))
		c.setopt(pycurl.POST, True)
		c.setopt(c.POSTFIELDS, postfields)
		c.perform()
		c.close()

		html = buffer.getvalue().decode('utf-8')

		### Parse chapter list
		root_obj = BeautifulSoup(html, 'html.parser')
		ignore = False  # newest chap is interested by default
		if self.end > 0:
			ignore = True # end chap specified --> default is ignore
		for a_obj in root_obj.find_all('a'):
			link = a_obj['href']
			arr = re.findall(r'-(\d+)/', link, re.I)
			if arr:
				ch = int(arr[-1])
				if not ignore:
					# interesting
					if ch < self.begin:
						ignore = True
				else:
					if (ch >= self.begin) and ((ch <= self.end) or (self.end <= 0)):
						ignore = False
			if ignore:
				continue

			title = a_obj.contents[0]

			print("title %s, link %s" % (title, link))

			self._chapter_list.append({'title': title, 'link': link})

	def _getChapterContent(self, title, url):
		result = u''

		html = get_html_page(url, True)
		root_obj = BeautifulSoup(html, 'html.parser')

		content_obj = root_obj.find('div', attrs={'id': 'js-truyencv-content'})
		if not content_obj:
			raise Exception("Can't get content of chapter %s" % (url))

		result = u"<h5>%s</h5><br \\>" % (title)
		result += "<p>"
		for c in content_obj.contents:
			if isinstance(c, bs4.element.NavigableString):
				result += c.string + " <br />\n"
		
		# f = codecs.open('./tmp/' + title + ".html", "w", 'utf-8')
		# for c in content_obj.contents:
		# 	f.write("\n============%s\n" % (type(c)))
		# 	if isinstance(c, bs4.element.NavigableString):
		# 		f.write(c)
		# 	elif c:
		# 		f.write("IGN: " + c.name + " ")
		# 		#f.write(c.string)
		# f.close()

		return result