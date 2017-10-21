#!/usr/bin/python2
# -*- coding: utf-8 -*-
import re
import sys
import bs4
import traceback
import codecs

class TTVPost(object):
	"""Tang Thu Vien Post class"""
	def __init__(self, title='', content='', chapter=0):
		super(TTVPost, self).__init__()
		self.title = title
		self.content = content
		self.chapter = chapter

class TTVParser(object):
	"""Tang Thu Vien parser class"""
	chapter_list = []
	def __init__(self,):
		super(TTVParser, self).__init__()

	@staticmethod
	def parse_post(tag, parent=None):
		post = None
		content = u'<p>Trống rỗng</p>'
		postno = 0
		title = '__UN_TITLE__'

		if not tag:
			return None

		# find post number
		m = re.search(r'post_(\d+)', tag['id'])
		if not m:
			raise Exception("Post id %s cannot get post number" % (tag['id']))
		postno = m.groups()[0]
		chno = 0

		# Parse post
		tmp = "post_message_%s" % postno
		ftag = tag
		pm = ftag.find('div', id=tmp)
		if (not pm) and (parent):
			# Some time the root is wrong, also find in post parent
			ftag = parent
			# print("post %s need to find pm in parent" % postno)
			pm = ftag.find('div', id=tmp)
		if not pm:
			# with codecs.open("err_post_%s.html" % postno, "w", "utf-8") as fp:
			# 	fp.write(ftag.prettify())
			raise Exception("Post %s cannot get post message with id %s" % (postno, tmp))

		title_found = False
		for div in pm.find_all('div', attrs={'style': 'text-align: center;'}):
			# print("---->%s<----" % div.text)
			m = re.search(r'[cC]h.*ng\s+(\d+)\s*:?(.*)$', div.text, re.M)
			if m:
				# print("=====>%s" % (str(m.groups())))
				title = u"Chương %s: %s" % (m.groups()[0], m.groups()[1])
				chno = int(m.groups()[0])
				title_found = True
				break;
		if not title_found:
			# with codecs.open("err_post_%s.html" % postno, "w", "utf-8") as fp:
			# 	fp.write(pm.prettify())
			raise Exception("Post %s can not get chapter title" % (postno))

		# Check if the chapter is existed
		if len(TTVParser.chapter_list) > 0:
			if chno in TTVParser.chapter_list:
				raise Exception("Post %s chapter %d is already existed" % (postno, chno))
		TTVParser.chapter_list.append(chno)
		# print("Title: %s" % (title))

		# Viet phase usually first button
		t = pm.find('input')
		div = t.parent.parent
		# remove the button
		t.parent.clear()
		# delete style attribute
		def find_style_tag(tag):
			if 'style' in tag.attrs.keys():
				return True
			return False
		for t in div.find_all(find_style_tag):
			del t['style']
		content = "<p>" + div.prettify() + "</p>"

		post = TTVPost(title, content, chno)

		return post

	@staticmethod
	def parse_html(html_str=''):
		result = []

		soup = bs4.BeautifulSoup(html_str, 'html.parser')

		posts_tag = soup.find_all('li', id=re.compile("post_\d+"))

		for post_tag in posts_tag:
			post = None
			try:
				post = TTVParser.parse_post(post_tag, soup)
			except Exception as ex:
				print("ERR: %s" % (traceback.format_exc()))
			if post:
				result.append(post)

		return result

	@staticmethod
	def parse_url(url):
		html = u''
		if sys.version_info.major > 2:
			# python3
			import urllib.request
			fp = urllib.request.urlopen(url)
			mybytes = fp.read()
			html = mybytes.decode("utf8")
			fp.close()
		else:
			# python2
			import urllib
			fp = urllib.urlopen(url)
			mybytes = fp.read()
			try:
				html = mybytes.decode("utf8", errors="replace")
			except Exception as ex:
				print("ERR: %s" % (traceback.format_exc()))
			fp.close()

		return TTVParser.parse_html(html)
