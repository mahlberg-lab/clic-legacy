import json
import os

from cheshire3.baseObjects import Session
from cheshire3.document import StringDocument
from cheshire3.internal import cheshire3Root
from cheshire3.server import SimpleServer
from lxml import etree

BASE_DIR = os.path.dirname(__file__)
raw_booklist = open(os.path.join(BASE_DIR, 'booklist.json'), 'r')
booklist = json.load(raw_booklist)

"""Responsible for providing access to chapter resources within Cheshire."""
class ChapterRepository(object):

    def __init__(self):
        self.session = Session()
        self.session.database = 'db_dickens'
        self.serv = SimpleServer(self.session,
                             os.path.join(cheshire3Root, 'configs', 'serverConfig.xml')
                             )
        self.db = self.serv.get_object(self.session, self.session.database)
        self.qf = self.db.get_object(self.session, 'defaultQueryFactory')

    def get_book_title(self, book):
        """Gets the title of a book from the json file booklist.json

        book -- string - the book id/accronym e.g. BH
        """
        for b in booklist:
                if (b[0][0] == book):
                    book_title = b[0][1]

        return book_title

    def get_chapter(self, chapter_number, book):
        """Returns transformed XML for given chapter & book

        chapter_number -- integer
        book -- string - the book id/accronym e.g. BH
        """
        query = self.qf.get_query(self.session, 'c3.book-idx = "%s"' % book)
        result_set = self.db.search(self.session, query)
        chapter_ptr = result_set[chapter_number - 1]
        chapter = chapter_ptr.fetch_record(self.session)
        transformer = self.db.get_object(self.session, 'chapterView-Txr')
        formatted_chapter = transformer.process_record(self.session, chapter).get_raw(self.session)

        book_title = self.get_book_title(book)

        return formatted_chapter, book_title

    def get_raw_chapter(self, chapter_number, book):
        """ Returns raw chapter XML for given chapter & book

        chapter_number -- integer
        book -- string - the book id/accronym e.g. BH
        """
        query = self.qf.get_query(self.session, 'c3.book-idx = "%s"' % book)
        result_set = self.db.search(self.session, query)
        chapter_ptr = result_set[chapter_number - 1]
        chapter = chapter_ptr.fetch_record(self.session)
        return chapter.get_dom(self.session)

    def get_chapter_with_highlighted_search_term(self, chapter_number, book, wid, search_term):
        """ Returns transformed XML for given chapter & book with the search
        highlighted.

        We create the transformer directly so that we can pass extra parameters
        to it at runtime. In this case the search term.

        chapter_number -- integer
        book -- string - the book id/accronym e.g. BH
        wid -- integer - word index
        search_term -- string - term to highlight
        """
        raw_chapter = self.get_raw_chapter(chapter_number, book)

        """load our chapter xslt directly as a transformer"""
        # FIXME this is hard-coded
        xslt_doc = etree.parse('/home/jdejoode/code/clic-project/clic/dbs/dickens/xsl/chapterView.xsl')
        transformer = etree.XSLT(xslt_doc)

        terms = search_term.split(' ')

        """pass the search term into our transformer"""
        transformed_chapter = transformer(raw_chapter, wid="'%s'" % wid, numberOfSearchTerms="%s" % len(terms))
        book_title = self.get_book_title(book)

        """return transformed html"""
        return etree.tostring(transformed_chapter), book_title

