## TO CREATE bookcounts.json

import os
import re
from lxml import etree
import json

from cheshire3.document import StringDocument
from cheshire3.internal import cheshire3Root
from cheshire3.server import SimpleServer
from cheshire3.baseObjects import Session


### read info from booklist: cumulative word count in chapters
# booklist = open('/home/aezros/workspace/testClic/staticFiles_test/booklist2')
# booklist = json.load(booklist)
# for b1 in booklist:
#     
    

###

session = Session()
session.database = 'db_dickens'
serv = SimpleServer(session,
                            os.path.join(cheshire3Root, 'configs', 'serverConfig.xml')
                            )
db = serv.get_object(session, session.database)
qf = db.get_object(session, 'defaultQueryFactory')
resultSetStore = db.get_object(session, 'resultSetStore')       
idxStore = db.get_object(session, 'indexStore')
 
list_books = ['BH', 'BR', 'DC', 'DS', 'ED', 'GE', 'HT', 'LD', 'MC', 'NN',
              'OCS', 'OMF', 'OT', 'PP', 'TTC',
               
              'AgnesG', 'Antoni', 'arma', 'cran', 'Deronda', 'dracula', 'emma', 'frank', 'jane', 'Jude',
               'LadyAud', 'mary', 'NorthS', 'persuasion', 'pride', 'sybil', 'Tess', 'basker', 'Pomp', 'mill',
               'dorian', 'Prof', 'native', 'alli', 'Jekyll', 'wwhite', 'vanity', 'VivianG', 'wh'
             ]
 
titles = {'BH': 'Bleak House', 'BR': 'Barnaby Rudge', 'DC': 'David Copperfield', 'DS': 'Dombey and Son',
          'ED': 'The Mystery of Edwin Drood', 'GE': 'Great Expectations', 'HT': 'Hard Times', 'LD': 'Little Dorrit', 
          'MC': 'Martin Chuzzlewit', 'NN': 'Nicholas Nickleby', 'OCS': 'The Old Curiosity Shop', 'OMF': 'Our Mutual Friend', 
          'OT': 'Oliver Twist', 'PP': 'Pickwick Papers', 'TTC': 'A Tale of Two Cities',
           
          'AgnesG': 'Agnes Grey', 'Antoni': 'Antonina, or the Fall of Rome', 'arma': 'Armadale', 'cran': 'Cranford', 
          'Deronda': 'Daniel Deronda', 'dracula': 'Dracula', 'emma': 'Emma', 'frank': 'Frankenstein', 'jane': 'Jane Eyre',
          'Jude': 'Jude the Obscure', 'LadyAud': 'Lady Audley\'s Secret', 'mary': 'Mary Barton', 'NorthS': 'North and South',
          'persuasion': 'Persuasion', 'pride': 'Pride and Prejudice', 'sybil': 'Sybil, or the two nations',
          'Tess': 'Tess of the D\'Urbervilles', 'basker': 'The Hound of the Baskervilles', 'Pomp': 'The Last Days of Pompeii', 
          'mill': 'The Mill on the Floss', 'dorian': 'The Picture of Dorian Gray', 'Prof': 'The Professor',
          'native': 'The Return of the Native', 'alli': 'The Small House at Allington', 
          'Jekyll': 'The Strange Case of Dr Jekyll and Mr Hide', 'wwhite': 'The Woman in White',
          'vanity': 'Vanity Fair', 'VivianG': 'Vivian Grey', 'wh': 'Wuthering Heights'          
          }
  
list_all_books = []
#list_all_books.insert(0, 'dickens')
 
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
      
    ###
    query = qf.get_query(session, 'c3.book-idx = "{0}"'.format(b))
    results = db.search(session, query)   
    wordTotal = 0
    wordCumulative = []
    for i, r in enumerate(results):
        rec = r.fetch_record(session)
        tree = rec.get_dom(session).getroottree() 
                
        wordInChap = len(tree.xpath('//div/descendant::w')) 
        wordStartChap = wordTotal 
          
        wordTotal = wordStartChap + wordInChap
          
        wordCumulative.append(wordStartChap)
     
    ## find title
    book_title = ""
    for t in titles.iteritems():
        if b == t[0]:
            book_title = t[1]
            break             
       
    within_book.append([b, book_title, [all_words, quote_words, nonquote_words], wordCumulative])
        
    #break
      
list_all_books.append(within_book)
print json.dumps(list_all_books)
 
