from ebooklib import epub

class Chapter(object):
	"""docstring for Chapter"""
	def __init__(self, cid='', title='', file_name='', cobj=None):
		super(Chapter, self).__init__()
		self.id = cid
		self.title = title
		self.file_name = file_name
		self.cobj = cobj

class EpubGenerator(object):
	"""docstring for EpubGenerator"""
	def __init__(self, name='', author=''):
		super(EpubGenerator, self).__init__()
		self._name = name
		self._author = author
		self._book = epub.EpubBook()
		self._chapters = []

		# set metadata
		self._book.set_identifier('id123456')
		self._book.set_title(self._name)
		self._book.set_language('vi')
		self._book.add_author(author)

	def add_chapter(self, title='', cid='', content=''):
		file_name = 'chap_%s.xhtml' % (cid)
		# create chapter
		c1 = epub.EpubHtml(title=title, file_name=file_name, lang='hr')
		c1.content=content

		# add chapter
		self._book.add_item(c1)
		self._chapters.append(Chapter(cid, title, file_name, c1))

	def write_book(self, book_file=''):
		chaplists = []
		for ch in self._chapters:
			chaplists.append(ch.cobj)
		chapobj = tuple(chaplists)
		# define Table Of Contents
		self._book.toc = (
			(epub.Section(self._name),
			chapobj
			)
		)

		# add default NCX and Nav file
		self._book.add_item(epub.EpubNcx())
		self._book.add_item(epub.EpubNav())

		# define CSS style
		# style = 'BODY {color: white;}'
		# nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

		# # add CSS file
		# self._book.add_item(nav_css)

		# basic spine
		# self._book.spine = ['nav', c1]

		# write to the file
		epub.write_epub(book_file, self._book, {})

