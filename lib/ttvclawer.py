#!/usr/bin/python2
# -*- coding: utf-8 -*-

from lib.parser import TTVParser
from lib.epubgen2 import EpubGenerator

class TTVClawer(object):
	"""docstring for TTVClawer"""
	def __init__(self, thread_url, title, author='', output='.'):
		super(TTVClawer, self).__init__()
		self._thread_url = thread_url
		self._cur_page = 1
		self._title = title
		self._author = author
		self._output = output

	def start(self):
		self._cur_page = 1
		last_post = 0
		last_page = 0
		epub = EpubGenerator(self._title, self._author)
		while True:
			print("Clawing page %d" % (self._cur_page))
			url = "%s&page=%d" % (self._thread_url, self._cur_page)

			posts = TTVParser.parse_url(url)

			# Process posts
			for post in posts:
				print("   chapter %s, length %d" % (post.title, len(post.content)))
				epub.add_chapter(post.title, 'chuong%d' % post.chapter, post.content)

			# Check if chapter number does not increase for long time
			if len(TTVParser.chapter_list) > 0:
				if last_post != TTVParser.chapter_list[-1]:
					last_post = TTVParser.chapter_list[-1]
					last_page = self._cur_page
				elif last_page < (self._cur_page - 5):
					print("Seem last page is %d for chapter %d" % (last_page, last_post))
					break;

			# if self._cur_page > 10:
			# 	break;

			# Next page
			self._cur_page += 1

		# Check if any chapters are missing
		for i in range(1, last_post + 1):
			if i not in TTVParser.chapter_list:
				print("ERR: chapter %d does not existed" % i)

		epub.write_book(self._output)


