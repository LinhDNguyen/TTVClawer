import re
import urllib.request
from bs4 import BeautifulSoup

fp = urllib.request.urlopen("http://www.tangthuvien.vn/forum/showthread.php?t=133696&page=41")
mybytes = fp.read()

mystr = mybytes.decode("utf8")
fp.close()

with open("tmp/orig.html", "w") as fp:
	fp.write(mystr)

# print(mystr)
print("HTML -> %dbytes" % (len(mystr)))
soup = BeautifulSoup(mystr, 'html.parser')

with open("tmp/full.html", "w") as fp:
	fp.write(soup.prettify())
# find: <div id="postlist" class="postlist restrain">
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
