#!/usr/bin/python2
# -*- coding: utf-8 -*-
import os
import sys
import codecs
import logging
from lib.ttvclawer import TTVClawer

if __name__ == '__main__':

	clawer = TTVClawer('http://www.tangthuvien.vn/forum/showthread.php?t=133696', u'Nhất Niệm Vĩnh Hằng', u'Nhĩ Căn', "/mnt/d/works/ttv_epub_creator/tmp")
	clawer.start()
	print("===========DONE==========")
