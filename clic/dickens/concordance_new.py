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
raw_booklist = open(os.path.join(BASE_DIR, 'booklist.json'), 'r')
booklist = json.load(raw_booklist)


class Concordancer_New(object):

    def __init__(self):
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


    def build_and_run_query(self, terms, idxName, Materials, selectWords):
        """
        Builds a cheshire query and runs it.

        Its output is a tuple of which the first element is a resultset and
        the second element is number of search terms in the query.
        """
        
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
        query = self.qf.get_query(self.session, ' or '.join(subcorpus) + ' and/proxInfo ' + ' or '.join(term_clauses))
        result_set = self.db.search(self.session, query)

        return result_set, number_of_search_terms


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
        result_set, number_of_search_terms = self.build_and_run_query(terms, idxName, Materials, selectWords)

        ## get total number of hits (not yet used in interface)
        total_count = 0
        if len(result_set) > 0: #FIXME What does cheshire return if there are no results? None? or [] ?
            for result in result_set:
                total_count = total_count + len(result.proxInfo)

        ## search through each record (chapter) and identify location of search term(s)
        if len(result_set) > 0:
            count = 0
            for result in result_set:

                ## get xml record
                rec = result.fetch_record(self.session)

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
                # * the second item in the deepest list (169, 171)
                #   is the id of the <w> (word) node
                # * the first item is the id of the root element from
                #   which to start counting to find the word node
                #   for instance, 0 for a chapter view (because the chapter
                #   is the root element), but 151 for a search in quotes
                #   text.
                # * the third element is the exact character (spaces, and
                #   and punctuation (stored in <n> (non-word) nodes
                #   at which the search term starts
                # * the fourth element is the total amount of characters
                #   in the document?

                for match in result.proxInfo:
                    count += 1

                    #FIXME will this code be run if there are more than 1000 results? will it not break out of the for loop?
                    #or will it break out of the if loop

                    if count > 1000: ## current search limit: 1000
                        break
                    else: #FIXME while this code be run if there are more than 1000 results? will it not break out of the for loop?

                        if idxName in ['chapter-idx']:
                            word_id = match[0][1]

                        elif idxName in ['quote-idx', 'non-quote-idx', 'longsus-idx', 'shortsus-idx']:
                            eid, word_id = match[0][0], match[0][1]

                            ## locate search term in xml
                            search_term = rec.process_xpath(self.session, '//*[@eid="%d"]/following::w[%d+1]' % (eid, word_id))

                            ## get xml of sentence
                            sentence_tree = rec.process_xpath(self.session, '//*[@eid="%d"]/following::w[%d+1]/ancestor-or-self::s' % (eid, word_id))
                            chapter_tree = rec.process_xpath(self.session, '//*[@eid="%d"]/following::w[%d+1]/ancestor-or-self::div' % (eid, word_id))

                            ## counts words preceding sentence
                            prec_s_tree = chapter_tree[0].xpath('/div/p/s[@sid="%s"]/preceding::s/descendant::w' % sentence_tree[0].get('sid'))
                            prec_s_wcount = len(prec_s_tree)

                            ## count words within sentence
                            count_s = 0
                            for word in chapter_tree[0].xpath('/div/p/s[@sid="%s"]/descendant::w' % sentence_tree[0].get('sid')):
                                if not word.get('o') == search_term[0].get('o'):
                                    count_s += 1
                                else:
                                    break

                            ## word number within chapter is adding word count in preceding sentence and word count in current sentence
                            wcount = prec_s_wcount + count_s
            			    #FIXME `w = wcount` dynamically reassigns a value to `w`
                            #that is already a value, namely the one refactored to `word_id`
                            word_id = wcount


                    ## Define leftOnset as w - 10, then get all w and n between that and node
                    leftOnset = max(1, word_id - word_window + 1) ## we operate with word position, not list position (word 1 = 0 position in list)
                    nodeOnset = word_id + 1
                    nodeOffset = word_id + number_of_search_terms
                    try:
                        rightOnset = nodeOffset + 1
                    except:
                        rightOnset = None

                    ch_words = len(rec.process_xpath(self.session, '/div/descendant::w')) ## move to level for each record (chapter) ?
                    rightOffset = min(rightOnset + word_window, rightOnset + (ch_words - rightOnset) + 1 )

                    left_text = []
                    for l in range(leftOnset, nodeOnset):
                        try:
                            left_n_pr = rec.process_xpath(self.session, '/div/descendant::w[%d]/preceding-sibling::n[1]' % l)[0].text
                        except:
                            left_n_pr = ''
                        left_w = rec.process_xpath(self.session, '/div/descendant::w[%d]' % l)[0].text
                        try:
                            left_n_fo = rec.process_xpath(self.session, '/div/descendant::w[%d]/following-sibling::n[1]' % l)[0].text
                        except:
                            left_n_fo = ''
                        left_text.append(''.join(left_n_pr + left_w + left_n_fo))


                    node_text = []
                    for n in range(nodeOnset, rightOnset):
                        try:
                            node_n_pr = rec.process_xpath(self.session, '/div/descendant::w[%d]/preceding-sibling::n[1]' % n)[0].text
                        except:
                            node_n_pr = ''
                        node_w = rec.process_xpath(self.session, '/div/descendant::w[%d]' % n)[0].text
                        try:
                            node_n_fo = rec.process_xpath(self.session, '/div/descendant::w[%d]/following-sibling::n[1]' % n)[0].text
                        except:
                            node_n_fo
                        node_text.append(''.join(node_n_pr + node_w + node_n_fo))

                    right_text = []
                    for r in range(rightOnset, rightOffset):
                        try:
                            right_n_pr = rec.process_xpath(self.session, '/div/descendant::w[%d]/preceding-sibling::n[1]' % r)[0].text
                        except:
                            right_n_pr = ''
                        right_w = rec.process_xpath(self.session, '/div/descendant::w[%d]' % r)[0].text
                        try:
                            right_n_fo = rec.process_xpath(self.session, '/div/descendant::w[%d]/following-sibling::n[1]' % r)[0].text
                        except:
                            right_n_fo = ''
                        right_text.append(''.join(right_n_pr + right_w + right_n_fo))

                    ###
                    book = rec.process_xpath(self.session, '/div')[0].get('book')
                    chapter = rec.process_xpath(self.session, '/div')[0].get('num')
                    para_chap = rec.process_xpath(self.session, '/div/descendant::w[%d+1]/ancestor-or-self::p' % word_id)[0].get('pid')
                    sent_chap = rec.process_xpath(self.session, '/div/descendant::w[%d+1]/ancestor-or-self::s' % word_id)[0].get('sid')
                    word_chap = word_id

                    ## count paragraph, sentence and word in whole book
                    count_para = 0
                    count_sent = 0
                    count_word = 0
                    booktitle = []
                    total_word = []
                    for b in booklist:
                        if b[0][0] == book:

                            booktitle.append(b[0][1])
                            total_word.append(b[1][0][2])

                            for j, c in enumerate(b[2]):
                                while j+1 < int(chapter):
                                    count_para = count_para + int(c[0])
                                    count_sent = count_sent + int(c[1])
                                    count_word = count_word + int(c[2])
                                    j += 1
                                    break

                                ## total word in chapter
                                if j+1 == int(chapter):
                                    chapWordCount = b[2][j][2]

                    book_title = booktitle[0]   ## get book title
                    total_word = total_word[0]
                    para_book = count_para + int(para_chap)
                    sent_book = count_sent + int(sent_chap)
                    word_book = count_word + int(word_chap)

                    conc_line = [left_text, node_text, right_text,
                                [book, book_title, chapter, para_chap, sent_chap, str(word_chap), str(chapWordCount)],
                                [str(para_book), str(sent_book), str(word_book), str(total_word)]]


                    conc_lines.append(conc_line)

        #conc_lines.insert(0, len(conc_lines))
        conc_lines.insert(0, total_count)
        return conc_lines
