import json
import os

from cheshire3.baseObjects import Session
from cheshire3.document import StringDocument
from cheshire3.internal import cheshire3Root
from cheshire3.server import SimpleServer

BASE_DIR = os.path.dirname(__file__)
raw_booklist = open(os.path.join(BASE_DIR, 'booklist.json'), 'r')
booklist = json.load(raw_booklist)

class Chapter_Repository(object):

    def __init__(self):
        self.session = Session()
        self.session.database = 'db_dickens'
        self.serv = SimpleServer(self.session,
                             os.path.join(cheshire3Root, 'configs', 'serverConfig.xml')
                             )
        self.db = self.serv.get_object(self.session, self.session.database)
        self.qf = self.db.get_object(self.session, 'defaultQueryFactory')
        
    def get_chapter(self, chapter_number, book):
        """ Returns transformed XML for given chapter & book """
        query = self.qf.get_query(self.session, 'c3.book-idx = "%s"' % book)
        result_set = self.db.search(self.session, query)
        chapter_ptr = result_set[chapter_number - 1]
        chapter = chapter_ptr.fetch_record(self.session)
        transformer = self.db.get_object(self.session, 'chapterView-Txr')
        formatted_chapter = transformer.process_record(self.session, chapter).get_raw(self.session)
        for b in booklist:
            if (b[0][0] == book):
                book_title = b[0][1]
        return formatted_chapter, book_title
        
    def get_raw_chapter(self, chapter_number, book):
        """ Returns raw chapter XML for given chapter & book """
        query = self.qf.get_query(self.session, 'c3.book-idx = "%s"' % book)
        result_set = self.db.search(self.session, query)
        chapter_ptr = result_set[chapter_number - 1]
        chapter = chapter_ptr.fetch_record(self.session)
        return chapter.get_dom(self.session)
        