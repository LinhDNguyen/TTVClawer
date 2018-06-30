#!/usr/bin/python2
# -*- coding: utf-8 -*-
import os
import sys
import codecs
import logging
from lib.ttvclawer import TTVClawer
from lib.ttvclawer2 import TTVClawer2

if __name__ == '__main__':

	# For old style TTV
	# clawer = TTVClawer('http://www.tangthuvien.vn/forum/showthread.php?t=143939', u'Mục Thần Ký', u'Thạch Trư', "/opt/p/tmp/TTVClawer/mtk")
	# For new style, using truyen.tangthuvien.vn
	clawer = TTVClawer2('https://truyen.tangthuvien.vn/doc-truyen/muc-than-ky', u'Mục Thần Ký', u'Thạch Trư', "./mtk")
	clawer.start()
	print("===========DONE==========")
