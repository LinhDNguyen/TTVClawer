#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import urllib
from bs4 import BeautifulSoup
# python2
import urllib
import codecs
import sys

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

html = get_html_page('https://truyen.tangthuvien.vn/doc-truyen/muc-than-ky/chuong-678')
root_obj = BeautifulSoup(html, 'html.parser')
fp = codecs.open("tmp/chapter_1.html", "w", "utf-8")
fp.write(root_obj.prettify())
fp.close()

content_obj = root_obj.find('div', attrs={'class': re.compile(r'.*box-chap.*')})
if not content_obj:
	print("ERR: can't find content obj")
	exit(0)
fp = codecs.open("tmp/content.html", "w", "utf-8")
fp.write(content_obj.prettify())
fp.close()

print(content_obj.text)

exit (0)

html = get_html_page('https://truyen.tangthuvien.vn/doc-truyen/page/17299?page=0&limit=1000&web=1')
root_obj = BeautifulSoup(html, 'html.parser')
fp = codecs.open("tmp/chapter.html", "w", "utf-8")
fp.write(root_obj.prettify())
fp.close()


### Parse chapter list
ul_obj = root_obj.find('ul', attrs={'class':'cf'})
if not ul_obj:
	raise Exception("Can't find ul element contains list chapter")
count = 1
# print(ul_obj.prettify())
for li_obj in root_obj.find_all('li'):
	# print(li_obj.prettify())
	# if count > 10:
	# 	break
	# count += 1
	a_obj = li_obj.find('a')
	link = a_obj['href']
	title = a_obj['title']

	print("%s --> %s" % (title, link))

exit(0)

mystr = ''
fp = urllib.urlopen("https://truyen.tangthuvien.vn/doc-truyen/muc-than-ky")
mybytes = fp.read()
try:
	mystr = mybytes.decode("utf8", errors="replace")
except Exception as ex:
	print("ERR: %s" % (traceback.format_exc()))
fp.close()

fp = codecs.open("tmp/orig.html", "w", "utf-8")
fp.write(mystr)
fp.close()

# print(mystr)
print("HTML -> %dbytes" % (len(mystr)))
soup = BeautifulSoup(mystr, 'html.parser')

fp = codecs.open("tmp/full.html", "w", "utf-8")
fp.write(soup.prettify())
fp.close()

# find: Danh sách chương
chap_list_obj = soup.find(string='Danh sách chương')
if not chap_list_obj:
	print("ERR: EMPTY CHAPPTER LIST")
	exit(0)
else:
	print(chap_list_obj)

list_obj = chap_list_obj.parent.parent
fp = codecs.open("tmp/list.html", "w", "utf-8")
fp.write(list_obj.prettify())
fp.close()

# Get maximum page
max_page_obj = list_obj.find(string="Trang cuối")
if not max_page_obj:
	print("ERR: can not find last page")
	exit(0)
max_pege_obj = max_page_obj.parent.parent
#Loading(10)
max_page_obj = re.match(r'Loading\(\s*(\d+)\s*\)', max_pege_obj['onclick'])
if not max_page_obj:
	print("ERR: can't get last page number")
max_page = int(max_page_obj.groups()[0])
print("Max PAGE NUMBER: %d" % max_page)

### Get story id
id_obj = soup.find('input', attrs={'id':'story_id_hidden', 'name':'story_id'})
print(id_obj['value'])

exit (0)
posts_div = soup.find('div', attrs={"id": "postlist"})
with open("tmp/div_out.html", "w") as fp:
	fp.write(posts_div.prettify())
if not posts_div:
	print("ERR: Can not found div");
posts_ol = posts_div.ol

# find all
def match_post_li(tag):
	# if tag.name != 'li':
	# 	return False
	if not tag.has_attr('id'):
		return False
	if not re.search(r'post_(\d+)', tag['id']):
		return False

	print("==>Found %s" % tag['id'])
	return True

print("have %d chirren" % (len(list(posts_ol.children))))
print("attr", str(posts_ol.attrs))
for li in posts_ol.children:
	print("%s => %s" % (li.name, len(li)))

posts = soup.find_all('li', id=re.compile("post_\d+"))
print("have %d posts" % len(posts))

post_lis = soup.find_all(match_post_li)
print("have %d posts" % (len(post_lis)))
# for post in post_lis:
# 	print(post)