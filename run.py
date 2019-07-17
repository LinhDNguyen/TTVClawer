#!/usr/bin/python2
# -*- coding: utf-8 -*-
import os
import sys
import codecs
import logging
from lib.ttvclawer2 import TTVClawer2, TruyenCVClawer

if __name__ == '__main__':

	# For old style TTV
	# clawer = TTVClawer('http://www.tangthuvien.vn/forum/showthread.php?t=143939', u'Mục Thần Ký', u'Thạch Trư', "/opt/p/tmp/TTVClawer/mtk")
	# For new style, using truyen.tangthuvien.vn, tangthuvien now isn't up-to-date
	#clawer = TTVClawer2('https://truyen.tangthuvien.vn/doc-truyen/muc-than-ky', u'Mục Thần Ký', u'Thạch Trư', "./mtk", start=1729)
	# From now on, TruyenCV is used
	#clawer =  TruyenCVClawer('https://truyencv.com/muc-than-ky/', u'Mục Thần Ký', u'Thạch Trư', "./mtk", start=1729)
	clawer = TruyenCVClawer('https://truyencv.com/de-ba/', u'Đế Bá', u'Yếm Bút Tiêu Sinh', './db', start=3600)
	clawer.start()
	print("===========DONE==========")
