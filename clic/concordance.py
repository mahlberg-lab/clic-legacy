# -*- coding: utf-8 -*-

'''
CLiC Concordance based on cheshire3 indexes.
'''

import json
import os

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

            out['title'] = b[0][1]
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
                                 os.path.join(cheshire3Root, 'configs', 'serverConfig.xml')
                                 )
        self.db = self.serv.get_object(self.session, self.session.database)
        self.qf = self.db.get_object(self.session, 'defaultQueryFactory')
        self.resultSetStore = self.db.get_object(self.session, 'resultSetStore')
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

	    #TODO change the variable names of the function itself (Materials -> selection, etc.)

        conc_lines = [] # return concordance lines in list
        word_window = 10 # word_window is set to 10 by default - on both sides of node

        query, number_of_search_terms = self.build_query(terms, idxName, Materials, selectWords)
        result_set = self.db.search(self.session, query)

        ## get total number of hits (not yet used in interface)
        total_count = 0
        if len(result_set) > 0: #FIXME What does cheshire return if there are no results? None? or [] ?
            for result in result_set:
                total_count = total_count + len(result.proxInfo)

        ## search through each record (chapter) and identify location of search term(s)
        if len(result_set) > 0:
            for result in result_set:

                # A record for a result is the entire chapter
                rec = result.fetch_record(self.session)

                # Find the current chapter and get stats for it
                ch_node = rec.process_xpath(self.session, '/div')[0]
                book = ch_node.get('book')
                chapter = ch_node.get('num')
                ch_stats = get_chapter_stats(book, chapter)

                # Get all tokens in the chapter as an array
                ch_tokens = rec.process_xpath(self.session, "/div/descendant::*[self::n or self::w]")
                # Generate a list of the locations of all word nodes
                ch_word_map = [
                    i for (i, n) in enumerate(ch_tokens)
                    if n.tag == 'w'
                ]

                # Each time a search term is found in a document
                # (each match) is described in terms of a proxInfo.
                #
                # It is insufficiently clear what proxInfo is.
                # It takes the form of three nested lists:
                #
                # [[[0, 169, 1033, 15292]],
                #  [[0, 171, 1045, 15292]], etc. ]
                #
                # We currently assume the following values:
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

                for match in result.proxInfo:
                    if idxName in ['chapter-idx']:
                        word_id = match[0][1]
                        search_term = rec.process_xpath(self.session, '/div/descendant::w[%d]' % (word_id + 1))[0]

                    elif idxName in ['quote-idx', 'non-quote-idx', 'longsus-idx', 'shortsus-idx']:
                        eid, word_id = match[0][0], match[0][1]
                        # Nesting: div -> p(ara) -> s(entence) -> toks -> w

                        ## locate search term in xml, count all words before it
                        search_term = rec.process_xpath(self.session, '//*[@eid="%d"]/following::w[%d]' % (eid, word_id + 1))
                        if len(search_term) != 1:
                            raise ValueError("eid %d was not found / not unique")
                        search_term = search_term[0]
                        word_id = int(search_term.xpath('count(preceding::w)'))

                    # context_left word word | match_left word (whitespace:match_end) | context_right word word : context_end
                    context_left = ch_word_map[max(0, word_id - word_window)]
                    match_left = ch_word_map[word_id]
                    match_end = ch_word_map[word_id + number_of_search_terms - 1] + 1  # i.e. whitespace after end of match
                    context_end = ch_word_map[min(
                        len(ch_word_map) - 1,
                        word_id + number_of_search_terms + word_window
                    )]

                    para_chap = search_term.xpath('ancestor-or-self::p/@pid')[0]
                    sent_chap = search_term.xpath('ancestor-or-self::s/@sid')[0]
                    word_chap = word_id

                    book_title = ch_stats['title']
                    total_word = ch_stats['total_word']
                    para_book = ch_stats['count_para'] + int(para_chap)
                    sent_book = ch_stats['count_sent'] + int(sent_chap)
                    word_book = ch_stats['count_word'] + int(word_chap)

                    conc_line = [
                        [n.text for n in ch_tokens[context_left:match_left]],
                        [n.text for n in ch_tokens[match_left:match_end]],
                        [n.text for n in ch_tokens[match_end:context_end]],
                        [book, book_title, chapter, para_chap, sent_chap, str(word_chap), str(ch_stats['count_chap_word'])],
                        [str(para_book), str(sent_book), str(word_book), str(total_word)],
                    ]


                    conc_lines.append(conc_line)

        #conc_lines.insert(0, len(conc_lines))
        conc_lines.insert(0, total_count)
        return conc_lines
