#!/usr/bin/python2
# -*- coding: utf-8 -*-
import os
import sys
import codecs
import logging
from lib.parser import TTVParser
from lib.epubgen2 import EpubGenerator

if __name__ == '__main__':
	posts = TTVParser.parse_url('http://www.tangthuvien.vn/forum/showthread.php?t=133696&page=41')
	epub = EpubGenerator(u'Nhất Niệm Vĩnh Hằng', u'Nhĩ Căn')

	print("Have %d posts" % (len(posts)))
	i=1
	for post in posts:
		cid = "chuong%d" % i
		i += 1
		print("post of %s, %d bytes" % (post.title, len(post.content)))
		with codecs.open("tmp/%s.html" % cid, "w", "utf-8") as fp:
			fp.write(post.content)
		epub.add_chapter(post.title, cid, post.content)

	epub.write_book("/mnt/d/works/ttv_epub_creator/tmp")
