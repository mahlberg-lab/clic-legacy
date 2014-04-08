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

# list_books = ['BH', 'BR', 'DC', 'DS', 'ED', 'GE', 'HT', 'ld', 'MC', 'NN',
#               'OCS', 'OMF', 'OT', 'PP', 'TTC']
#    
# list_all_books = []
# for b in list_books:
#     query = qf.get_query(session, 'c3.book-idx = "{0}"'.format(b))
#     results = db.search(session, query)
#        
#     across_chap_list = []
#     within_chap_list = []
#     list_all = []
#     list_all.insert(0, [b, len(results)])
#        
#     paraTotal = 0 
#     sentTotal = 0
#     wordTotal = 0
#     for i, r in enumerate(results):
#         rec = r.fetch_record(session)
#         tree = rec.get_dom(session).getroottree() 
#            
#         paraInChap = len(tree.xpath('//div/descendant::p')) 
#         sentInChap = len(tree.xpath('//div/descendant::s'))
#         wordInChap = len(tree.xpath('//div/descendant::w')) 
#            
#         paraTotal = paraTotal + paraInChap
#         sentTotal = sentTotal + sentInChap
#         wordTotal = wordTotal + wordInChap
#            
#         within_chap_list.append([paraInChap, sentInChap, wordInChap])
#        
#     across_chap_list.append([paraTotal, sentTotal, wordTotal])
#     list_all.insert(1, across_chap_list)
#     list_all.insert(2, within_chap_list)
#        
#     #print list_all
#        
#     list_all_books.append(list_all)
#     
#     #break
#   
# #print len(list_all_books)
# # 
# # ###
# f = open('/home/aezros/clic/dickens/booklist', 'w')
#  
# json.dump(list_all_books, f)

f2 = open('/home/aezros/clic/dickens/booklist', 'r')
x = json.load(f2)
#print len(x)

book = 'BH'
list = ['3', '22', '84', '1827']

count_para = 0
count_sent = 0
count_word = 0
for b in x:
    booktitle = b[0][0]
    if booktitle == book:
        
        for i, c in enumerate(b[2]):
            while i+1 < int(list[0]):
                #print c
                count_para = count_para + int(c[0])
                count_sent = count_sent + int(c[1])
                count_word = count_word + int(c[2])
                i += 1
                break
            
count_para = count_para + int(list[1])       
count_sent = count_sent + int(list[2])
count_word = count_word + int(list[3])   
print count_para, count_sent, count_word
 
