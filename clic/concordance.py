# -*- coding: utf-8 -*-

'''
CLiC Concordance based on cheshire3 indexes.
'''

import json
import os
import os.path
import collections
import tempfile
import cPickle as pickle

from cheshire3.baseObjects import Session
from cheshire3.document import StringDocument
from cheshire3.internal import cheshire3Root
from cheshire3.server import SimpleServer


#### LOAD METADATA ####
# load the metadata about chapters, word counts, etc.
# from each individual book in the corpus
# 1. get the directory of the present file (stored in __file__)
# 2. open the 'booklist.json' file which contains the data we want
# 3. convert it to json
#
# For each book in the corpus there is the following information listed in booklist:
#
#     book id - e.g. "BH"
#     book title - "Bleak House"
#     number of chapters in book
#     total number of paragraphs
#     total number of sentences
#     total number of words
#
# Then for each chapter within the book booklist:
#
#     number of paragraphs
#     number of sentences
#     number of words

BASE_DIR = os.path.dirname(__file__)
CLIC_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
with open(os.path.join(BASE_DIR, 'booklist.json'), 'r') as raw_booklist:
    booklist = json.load(raw_booklist)

def get_chapter_stats(book, chapter):
    ## count paragraph, sentence and word in whole book
    out = dict(
        count_para=0,
        count_sent=0,
        count_word=0,
    )

    for b in booklist:
        if b[0][0] == book:

            out['book_title'] = b[0][1]
            out['total_word'] = b[1][0][2]

            for j, c in enumerate(b[2]):
                while j+1 < int(chapter):
                    out['count_para'] += int(c[0])
                    out['count_sent'] += int(c[1])
                    out['count_word'] += int(c[2])
                    j += 1
                    break

                ## total word in chapter
                if j+1 == int(chapter):
                    out['count_chap_word'] = b[2][j][2]
            return out

    raise ValueError("Cannot find book stats")


class Chapter():
    """
    Abstracts a cheshire3 Chapter record, performing all lookups CLiC needs

    Designed to be picked and re-used to save work
    """
    def __init__(self, dom, digest):
        """
        Create object
        - dom: The lxml Root node for the chapter (a div)
        - digest: The record digest, used to check for updates
        """
        self.digest = digest
        ch_node = dom.xpath('/div')[0]
        self.book = ch_node.get('book')
        self.chapter = ch_node.get('num')
        for (k,v) in get_chapter_stats(self.book, self.chapter).items():
            setattr(self, k, v)

        self.tokens = []
        self.word_map = []
        for n in dom.xpath("/div/descendant::*[self::n or self::w]"):
            self.tokens.append(n.text)
            if n.tag == 'w':
                self.word_map.append(len(self.tokens) - 1)

        self.para_words = []
        self.sentence_words = []
        for para_node in dom.xpath("/div/p"):
            self.para_words.append(int(para_node.xpath("count(descendant::w)")))
            for sentence_node in para_node.xpath("s"):
                self.sentence_words.append(int(sentence_node.xpath("count(descendant::w)")))

        self.eid_pos = {}
        for eid_node in dom.xpath("//*[@eid]"):
            self.eid_pos[eid_node.get('eid')] = int(eid_node.xpath('count(preceding::w)'))

    def get_word(self, match):
        """
        Given a CLiC proxInfo match, return an array of:
        - word_id: word position in chapter
        - para_chap: word's paragraph position in chapter
        - sent_chap: word's sentence position in chapter
        """
        # Each time a search term is found in a ProximityIndex
        # (each match) is described in terms of a proxInfo.
        #
        # [[[0, 169, 1033, 15292]],
        #  [[0, 171, 1045, 15292]], etc. ]
        #
        # * the first item is the id of the root element from
        #   which to start counting to find the word node
        #   for instance, 0 for a chapter view (because the chapter
        #   is the root element), but 151 for a search in quotes
        #   text.
        # * the second item in the deepest list (169, 171)
        #   is the id of the <w> (word) node
        # * the third element is the exact character (spaces, and
        #   and punctuation (stored in <n> (non-word) nodes
        #   at which the search term starts
        # * the fourth element is the total amount of characters
        #   in the document?
        #
        # See:-
        # dbs/dickens/dickensConfigs.d/dickensIdxs.xml
        # cheshire3.index.ProximityIndex
        #
        # It's [nodeIdx, wordIdx, offset, termId(?)] in transformer.py
        def find_position_in(list_of_counts, id):
            # NB: We return a position 1..n, not array position
            total = 0
            for (i, count) in enumerate(list_of_counts):
                total += count
                if total > id:
                    return i + 1
            return len(list_of_counts)

        #NB: cheshire source suggests that there's never multiple, but I can't say for sure
        eid, word_id = match[0][0:2]
        if eid > 0:
            word_id += self.eid_pos[str(eid)]

        return (
            word_id,
            find_position_in(self.para_words, word_id),
            find_position_in(self.sentence_words, word_id),
        )

    def get_conc_line(self, word_id, node_size, word_window):
        """
        Given (word_id) generated by get_word(), return:
          - (word_window) word tokens before word_id match
          - (node_size) word tokens within match
          - (word_window) word tokens after match
        """
        def find_split(left_pos, right_pos):
            # Match start starts at the final left word, and advances until either:
            #  (a) We get to node_start
            #  (b) We find a space, in which case we use the token after
            # <minute> <!> [Come] . . .
            # <minute> <!> <?> [Come] . . .
            # <girls> <,> < > ["] <Come> . . . .
            i = left_pos
            while i < right_pos:
                if self.tokens[i].isspace():
                    return i + 1
                i += 1
            return i

        # First, work out word positions in left/node/right sections
        max_word_map = len(self.word_map) - 1
        left_start = self.word_map[max(0, word_id - word_window)]
        left_end = self.word_map[max(0, word_id - 1)]
        node_start = self.word_map[word_id]
        node_end = self.word_map[min(max_word_map, word_id + node_size - 1)]
        right_start = self.word_map[min(max_word_map, word_id + node_size)]
        right_end = self.word_map[min(max_word_map, word_id + node_size + word_window)]

        # Then adjust node_start and right_start to take into account associated non-word tokens
        node_start = find_split(left_end, node_start)
        right_start = find_split(node_end, right_start)

        return [
            self.tokens[left_start:node_start],
            self.tokens[node_start:right_start],
            self.tokens[right_start:right_end],
        ]

chapter_cache = {}
def get_chapter(session, result, force=False):
    """
    Given a Cheshire3 (session) and resultSetItem (result),
    return a Chapter object, either from cache or fresh.
    """
    if force or result.id not in chapter_cache:
        chapter_pickle_file = os.path.join(tempfile.gettempdir(), 'clic-chapter-cache-%d.pickle' % result.id)

        if force or not(os.path.exists(chapter_pickle_file)):
            record = result.fetch_record(session)
            chapter_cache[result.id] = Chapter(record.dom, record.digest)
            with open(chapter_pickle_file, 'wb') as f:
                pickle.dump(chapter_cache[result.id], f)
        else:
            with open(chapter_pickle_file, 'rb') as f:
                chapter_cache[result.id] = pickle.load(f)

    # Test checksum, if it doesn't match the load the document afresh
    recStore = session.server.get_object(session, result.database).get_object(session, result.recordStore)
    if chapter_cache[result.id].digest != recStore.fetch_recordMetadata(session, result.id, 'digest'):
        return get_chapter(session, result, force=True)

    return chapter_cache[result.id]


class Concordance(object):
    '''
    This concordance takes terms, index names, book selections, and search type
    as input values and returns json with the search term, ten words to the left and
    ten to the right, and location information.

    This can be used in an ajax api.
    '''

    def __init__(self):
        '''
        Set up a cheshire3 session/connection to the database. This initilisation does
        not handle the actual search term (cf. build_query).
        '''

        self.session = Session()
        self.session.database = 'db_dickens'
        self.serv = SimpleServer(self.session,
                                 os.path.join(CLIC_DIR, 'cheshire3-server', 'configs', 'serverConfig.xml')
                                 )
        self.db = self.serv.get_object(self.session, self.session.database)
        self.qf = self.db.get_object(self.session, 'defaultQueryFactory')
        self.idxStore = self.db.get_object(self.session, 'indexStore')
        #self.logger = self.db.get_object(self.session, 'concordanceLogger')


    def build_query(self, terms, idxName, Materials, selectWords):
        '''
        Builds a cheshire query
         - terms: Search terms (space separated?)
         - idxName: Index to use, e.g. "chapter-idx"
         - Materials: List of subcorpi to search, e.g. ["dickens"]
         - selectWords: "whole" / "any"

        Its output is a tuple of which the first element is a query.
        the second element is number of search terms in the query.
        '''

        subcorpus = []
        for corpus in Materials:
            MatIdx = 'book-idx'
            # ntc is 19th century?
            if corpus in ['dickens', 'ntc']:
                MatIdx_Vol = 'subCorpus-idx'
                subcorpus.append('c3.{0} = "{1}"'.format(MatIdx_Vol, corpus))
            else:
                subcorpus.append('c3.{0} = "{1}"'.format(MatIdx, corpus))

        ## search whole phrase or individual words?
        if selectWords == "whole":
            # for historic purposes: number_of_search_terms was originally nodeLength
            number_of_search_terms = len(terms.split())
            terms = [terms]
        else:
            #FIXME is this correct in case of an AND search?
            number_of_search_terms = 1
            terms = terms.split()

        ## define search term
        term_clauses = []
        for term in terms:
            term_clauses.append('c3.{0} = "{1}"'.format(idxName, term))

        ## conduct database search
        ## note: /proxInfo needed to search individual books
        query = self.qf.get_query(self.session, '(%s) and/proxInfo (%s)' % (
            ' or '.join(subcorpus),
            ' or '.join(term_clauses),
        ))

        return query, number_of_search_terms


    def create_concordance(self, terms, idxName, Materials, selectWords):
        """
        main concordance method
        create a list of lists containing each three contexts left - node -right,
        and a list within those contexts containing each word.
        Add two separate lists containing metadata information:
        [
        [left context - word 1, word 2, etc.],
        [node - word 1, word 2, etc],
        [right context - word 1, etc],
        [chapter metadata],
        [book metadata]
        ],
        etc.
        """
        ##self.logger.log(10, 'CREATING CONCORDANCE FOR RS: {0} in {1} - {2}'.format(terms, idxName, Materials))

        query, number_of_search_terms = self.build_query(terms, idxName, Materials, selectWords)
        result_set = self.db.search(self.session, query)

        conc_lines = [] # return concordance lines in list
        word_window = 10 # word_window is set to 10 by default - on both sides of node

        if sum(len(result.proxInfo) for result in result_set) > 10000:
            raise ValueError("This query returns over 10 000 results, please try some other search terms using less-common words.")

        ## search through each record (chapter) and identify location of search term(s)
        for result in result_set:
            ch = get_chapter(self.session, result)

            for match in result.proxInfo:
                (word_id, para_chap, sent_chap) = ch.get_word(match)

                para_book = ch.count_para + int(para_chap)
                sent_book = ch.count_sent + int(sent_chap)
                word_book = ch.count_word + int(word_id)
                conc_line = ch.get_conc_line(word_id, number_of_search_terms, word_window) + [
                    [ch.book, ch.book_title, ch.chapter, str(para_chap), str(sent_chap), str(word_id), str(ch.count_chap_word)],
                    [str(para_book), str(sent_book), str(word_book), str(ch.total_word)],
                ]

                conc_lines.append(conc_line)

        conc_lines.insert(0, len(conc_lines))  # NB: This was an aborted attempt to provide server-side pagination, keep it here for now.
        return conc_lines
