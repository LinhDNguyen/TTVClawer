import pypub

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
		self._book = pypub.Epub(name)
		self._chapters = []

	def add_chapter(self, title='', cid='', content=''):
		file_name = 'chap_%s.xhtml' % (cid)
		# create chapter
		cobj = pypub.Chapter(content, title)

		# add chapter
		self._book.add_chapter(cobj)
		self._chapters.append(Chapter(cid, title, file_name, cobj))

	def write_book(self, book_file=''):
		self._book.create_epub(book_file)

