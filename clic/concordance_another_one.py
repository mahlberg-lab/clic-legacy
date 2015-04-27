# coding: utf-8

## Brand New Concordance

# A quick and dirty way of building a concordance

# TODO:
# Specs / Questions / Todos
# -------------------------
#
# * what if the search terms are more complex? how do you then do their len()?
# * handle quotes etc.
# * doing pagination
# * adding query builder
# * highlighting in a form if a word is frequent and it will thus take some time
# * searches for more than a word (either a phrase or an or search)
# * a transformer somewhere?
# * limit the cheshire results to specific numbers?
# * highlight for the user that a heavy query is loading
# * check whether there is only one result
# * cut off on words, not characters

import os

from cheshire3.baseObjects import Session
from cheshire3.document import StringDocument
from cheshire3.internal import cheshire3Root
from cheshire3.server import SimpleServer

session = Session()
session.database = 'db_dickens'
serv = SimpleServer(session, os.path.join(cheshire3Root, 'configs', 'serverConfig.xml'))
db = serv.get_object(session, session.database)
qf = db.get_object(session, 'defaultQueryFactory')
resultSetStore = db.get_object(session, 'resultSetStore')
idxStore = db.get_object(session, 'indexStore')

def build_concordance(term, context):

    query = qf.get_query(session, """(c3.subcorpus-idx all "dickens" and/cql.proxinfo c3.chapter-idx any "{}" )""".format(term))
    result_set = db.search(session, query)

    concordance = []

    for result in result_set:
        record = result.fetch_record(session)
        tree = record.get_dom(session)
        text_nodes = tree.xpath('//txt/text()')
        text_only = ' '.join(sentence for sentence in text_nodes)

        for hit in result.proxInfo:
            word_id = hit[0][1]
            char_location = hit[0][2]
            concordance_line = text_only[char_location - context : char_location + len(term) + context]
            #NOTE in these cases record.process_xpath(session, xpath) is not faster
            #TODO check there is only one result
            #sentence = tree.xpath('/div/descendant::w[%i]/ancestor-or-self::s/@id' % int(word_id + 1))
            #paragraph = tree.xpath('/div/descendant::w[%i]/ancestor-or-self::p/@id' % int(word_id + 1))
            #concordance.append((concordance_line, sentence[0], paragraph[0]))
            concordance.append(concordance_line)

    return concordance


concordance = build_concordance("the", 25)
print len(concordance)

def build_concordance_with_locations(term, context, max_hits):

    query = qf.get_query(session, """(c3.subcorpus-idx all "dickens" and/cql.proxinfo c3.chapter-idx any "{}" )""".format(term))
    result_set = db.search(session, query)

    concordance = []

    count = 0

    for result in result_set:

        if count < max_hits:
            record = result.fetch_record(session)
            tree = record.get_dom(session)
            text_nodes = tree.xpath('//txt/text()')
            text_only = ' '.join(sentence for sentence in text_nodes)

            for hit in result.proxInfo:
                if count < max_hits:
                    count +=1

                    word_id = hit[0][1]
                    char_location = hit[0][2]
                    concordance_line = text_only[char_location - context : char_location + len(term) + context]
                    #NOTE in these cases record.process_xpath(session, xpath) is not faster
                    #TODO check there is only one result
                    sentence = tree.xpath('/div/descendant::w[%i]/ancestor-or-self::s/@id' % int(word_id + 1))
                    paragraph = tree.xpath('/div/descendant::w[%i]/ancestor-or-self::p/@id' % int(word_id + 1))
                    concordance.append((concordance_line, sentence[0], paragraph[0]))

    return concordance


build_concordance_with_locations("fog", 25, 100)
concordance = build_concordance_with_locations("the", 25, 1000)
len(concordance)
for line in concordance[:10]:
    print line

