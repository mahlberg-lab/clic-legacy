import os
import re
from lxml import etree
import json

from cheshire3.document import StringDocument
from cheshire3.internal import cheshire3Root
from cheshire3.server import SimpleServer
from cheshire3.baseObjects import Session

session = Session()
session.database = 'db_dickens'
serv = SimpleServer(session,
                            os.path.join(cheshire3Root, 'configs', 'serverConfig.xml')
                            )
db = serv.get_object(session, session.database)
qf = db.get_object(session, 'defaultQueryFactory')
resultSetStore = db.get_object(session, 'resultSetStore')       
idxStore = db.get_object(session, 'indexStore')

list_books = ['BH', 'BR', 'DC', 'DS', 'ED', 'GE', 'HT', 'ld', 'MC', 'NN',
              'OCS', 'OMF', 'OT', 'PP', 'TTC']

list_all_books = []
list_all_books.insert(0, 'dickens')

within_book = []
for b in list_books:    
          
    query = qf.get_query(session, 'c3.book-idx = "%s"' % b)
    results = db.search(session, query)
    sent_idx = db.get_object(session, 'sentence-idx')
    quote_idx = db.get_object(session, 'quote-idx')
    nonquote_idx = db.get_object(session, 'non-quote-idx')
       
    sent_facets = sent_idx.facets(session, results)   
    all_words = 0    
    for x in sent_facets:
        all_words += x[1][2]
       
    quote_facets = quote_idx.facets(session, results)    
    quote_words = 0
    for x in quote_facets:
        quote_words += x[1][2]
       
    nonquote_facets = nonquote_idx.facets(session, results)
    nonquote_words = 0
    for x in nonquote_facets:
        nonquote_words += x[1][2]
           
          
    print b, all_words, quote_words, (all_words-quote_words)
       
    within_book.append([b, [all_words, quote_words, (all_words - quote_words)]])
           
    #break
   
list_all_books.append(within_book)
print json.dumps(list_all_books)

quote_total = 0
nonquote_total =0    
for b in list_all_books[1]:
    quote_total += b[1][1]
    nonquote_total += b[1][2]

print (quote_total + nonquote_total), quote_total, nonquote_total

###
# dir_19c = '/home/aezros/Documents/19thCentury_AnnotationOrig/Quotes_NonQ_txtfiles/'
#   
# book_count = []
# for file in os.listdir(dir_19c):
#       
#      
#     nonquote_words = 0
#     quote_words = 0
#       
#     book = re.sub('\_.+$', '', os.path.basename(file))
#           
#     if os.path.basename(file).endswith('_NonQuotes.txt'):
#         read = open(''.join(dir_19c + os.path.basename(file)), 'r').read()
#         split = read.split(' ')
#         nonq_words = len(split)
#           
#         nonquote_words += nonq_words
#         #print os.path.basename(file), nonquote_words   
#         book_count.append([book, [(nonquote_words + nonquote_words/3), nonquote_words/3, nonquote_words] ])  
# 
# quote_total = 0
# nonquote_total =0    
# for b in book_count:
#     quote_total += b[1][1]
#     nonquote_total += b[1][2]
#     
# all_total = quote_total + nonquote_total
# 
# book_count.insert(0, ['ntc', [all_total, quote_total, nonquote_total]])
# print book_count
#        
# #print json.dumps(book_count)
