import os
import re
import timeit

from cheshire3.document import StringDocument
from cheshire3.internal import cheshire3Root
from cheshire3.server import SimpleServer
from cheshire3.baseObjects import Session

from lxml import etree

import json

wd = os.getcwd()

booklist_r = open(''.join(wd + '/clic/dickens/booklist'), 'r')
#booklist_r = open('/home/aezros/clic/clic/dickens/booklist', 'r')
#booklist_r = open('booklist', 'r')
booklist = json.load(booklist_r)

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
        ## self.logger = self.db.get_object(self.session, 'concordanceLogger') ## TODO: add to dbs/dickens/config        
       
    def create_concordance(self, terms, idxName, Materials, selectWords): 
        ## create a list of lists containing each three contexts, and a list within those contexts containing each word
        session = self.session
        db = self.db
        qf = self.qf        
        
        #extraSpaceElems = ['s']
        conc_lines = []
        wordWindow = 10      
    
        
        Dickens_vol = ['BH', 'BR', 'DC',
                        'DS', 'ED', 'GE', 'HT', 'ld', 'MC', 'NN',
                        'OCS', 'OMF', 'OT', 'PP', 'TTC']
        books = []
        for Material in Materials:
            MatIdx = 'book-idx'
            if Material in ['dickens', 'ntc']:
                for book in Dickens_vol:
                    books.append('c3.{0} = "{1}"'.format(MatIdx, book))  
            else:
                books.append('c3.{0} = "{1}"'.format(MatIdx, Material)) 
                
        if selectWords == "whole":
            nodeLength = len(terms.split(' '))
            terms = [terms]  
        else:
            nodeLength = 1
            terms = terms.split(' ')
        
        term_clauses = []
        for term in terms:
            term_clauses.append('c3.{0} = "{1}"'.format(idxName, term))      

        
        ## /proxInfo needed to search individual books
        query = qf.get_query(session, ' or '.join(books) + ' and/proxInfo ' + ' or '.join(term_clauses))         
        rs = db.search(session, query)  
    
        if len(rs) > 0:
            count = 0
            for i in rs:
                
                rec = i.fetch_record(session)
                tree = rec.get_dom(session).getroottree()     
                #print tree.xpath('//div')[0].get('id')       
               
                for m in i.proxInfo: 
                    count += 1
                    
                    if idxName in ['chapter-idx']:    
                        w = m[0][1]                                          
               
                    elif idxName in ['quote-idx', 'non-quote-idx', 'longsus-idx', 'shortsus-idx']:  
                        elems = [0] 
                        (e_q, w_q) = (m[0][0], m[0][1])                    
                        
                        ## locate search term in xml
                        search_term = tree.xpath('//*[@eid="%d"]/following::w[%d+1]' % (e_q, w_q))   

                        sentence_tree = tree.xpath('//*[@eid="%d"]/following::w[%d+1]/ancestor-or-self::s' % (e_q, w_q))    
                        chapter_tree = tree.xpath('//*[@eid="%d"]/following::w[%d+1]/ancestor-or-self::div' % (e_q, w_q))                         
                       
                        prec_s_tree = chapter_tree[0].xpath('//div//s[@sid="%s"]/preceding::s/descendant::w' % sentence_tree[0].get('sid'))
                        prec_s_wcount = len(prec_s_tree)

                        ## count words within sentence
                        count_s = 0                        
                        for word in chapter_tree[0].xpath('//div//s[@sid="%s"]/descendant::w' % sentence_tree[0].get('sid')):
                            if not word.get('o') == search_term[0].get('o'):
                                count_s += 1
                            else:
                                break

                        wcount = prec_s_wcount + count_s
                                    
                        w = wcount
                        
#                     ## Alternative method of getting location of concordances: identify string location
#                     ## Instead we identify text by counting words, and including non-word symbols from xml
#                     ## get indexes
#                     if idxName in ['quote-idx', 'non-quote-idx', 'longsus-idx', 'shortsus-idx']: 
#                         index = db.get_object(session, 'chapter-idx')                 
#                     else:
#                         index = db.get_object(session, '%s' % (idxName))
                        
#                     vecs = {}  
#                     for el in elems:
#                         vecs[el] = self.idxStore.fetch_proxVector(session, index, i, e)   
#                     v = vecs[el] 
#                     
#                     nodeLength = len(m)            
                
#                     finalOffset=0
#                     try:
#                         tid = v[w+nodeLength+wordWindow]         
#                         finalOffset=tid[2]
#                     except:
#                         finalOffset = None
#                       
#                     ## test if node is at the end of string (i.e. node offset corresponds with right-hand offset)
#                     lastNodeOffset = v[w+nodeLength-1][2]
#                     rightHandOffset = v[min(w+nodeLength, len(v)-1)][2]
#                     if rightHandOffset == lastNodeOffset:
#                         rightHandOffset = None
                            
#                     ## string location
#                     wordWindow = int(wordWindow)
#                     leftOnset = v[max(0, w-(wordWindow))][2]  ## 10 words
#                     leftOffset = v[w][2]
#                     nodeOffset = v[min(w+nodeLength, len(v)-1)][2]
#                     rightOffset = v[min(w+nodeLength+wordWindow, len(v)-1)][2]
# #                     finalOffset = finalOffset

                    
#                     proxOffset = [leftOnset, leftOffset, nodeOffset, rightOffset]
# 
#                     if idxName in ['sentence-idx']:
#                         tree = tree.xpath('//*[@eid=%s]' % i.proxInfo[0][0][0])[0]
#                     else:
#                         tree
#                      
#                     walker = tree.getiterator()
#                     texts = []
#                     for c in walker:
#                         if c.tag == 'txt':                       
#                             if c.text:
#                                 texts.append(c.text)                        
#                             if c.tail:
#                                 texts.append(c.tail)
#                        
#                         ## add space to sentence
#                         elif c.tag in extraSpaceElems :
#                             texts.append(' ')
#                         else:
#                             continue     
#                       
#                     text = ''.join(texts).lstrip()
#                     left_text = [text[proxOffset[0]:proxOffset[1]]]
#                     node_text = [text[proxOffset[1]:proxOffset[2]]]
#                     #print node_text
#                     right_text = [text[proxOffset[2]:proxOffset[3]]]

                    #conc_line = [re.split('\s|^|$', left_text[0]), re.split('\s|^|$', node_text[0]), re.split('\s|^|$', right_text[0])]
                    
                    ## Define leftOnset as w - 10, then get all w and n between that and node
                    wordWindow = int(wordWindow)
                    leftOnset = max(0, w-wordWindow+1)
                    nodeOnset = w+1
                    nodeOffset = w+nodeLength
                    try:
                        rightOnset = nodeOffset + 1
                    except:
                        rightOnset = None
                         
                    ch_words = len(tree.xpath('//div/descendant::w')) ## move to level for each record (chapter) ?                      
                    rightOffset = min(rightOnset + wordWindow, rightOnset + (ch_words - rightOnset) + 1 )
                      
                    left_text = []   
                    for l in range(leftOnset, nodeOnset):
                        try:
                            left_n_pr = tree.xpath('//div/descendant::w[%d]/preceding-sibling::n[1]' % l)[0].text
                        except:
                            left_n_pr = ''  
                        left_w = tree.xpath('//div/descendant::w[%d]' % l)[0].text
                        try: 
                            left_n_fo = tree.xpath('//div/descendant::w[%d]/following-sibling::n[1]' % l)[0].text   
                        except:
                            left_n_fo = ''                 
                        left_text.append(''.join(left_n_pr + left_w + left_n_fo))
                            
                             
                    node_text = [] 
                    for n in range(nodeOnset, rightOnset):
                        try:
                            node_n_pr = tree.xpath('//div/descendant::w[%d]/preceding-sibling::n[1]' % n)[0].text     
                        except:
                            node_n_pr = ''             
                        node_w = tree.xpath('//div/descendant::w[%d]' % n)[0].text
                        try:
                            node_n_fo = tree.xpath('//div/descendant::w[%d]/following-sibling::n[1]' % n)[0].text
                        except:
                            node_n_fo
                        node_text.append(''.join(node_n_pr + node_w + node_n_fo))
                                          
                    right_text = [] 
                    for r in range(rightOnset, rightOffset): 
                        try:
                            right_n_pr = tree.xpath('//div/descendant::w[%d]/preceding-sibling::n[1]' % r)[0].text
                        except:
                            right_n_pr = ''                        
                        right_w = tree.xpath('//div/descendant::w[%d]' % r)[0].text
                        try:
                            right_n_fo = tree.xpath('//div/descendant::w[%d]/following-sibling::n[1]' % r)[0].text
                        except:
                            right_n_fo = ''
                        right_text.append(''.join(right_n_pr + right_w + right_n_fo))
                    
                    ### 
                    book = tree.xpath('//div')[0].get('book')
                    chapter = tree.xpath('//div')[0].get('num')
                    para_chap = tree.xpath('//div//descendant::w[%d+1]/ancestor-or-self::p' % w)[0].get('pid')
                    sent_chap = tree.xpath('//div//descendant::w[%d+1]/ancestor-or-self::s' % w)[0].get('sid')
                    word_chap = w                 
                    
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
                    
                    book_title = booktitle[0]   ## get book title 
                    total_word = total_word[0]     
                    para_book = count_para + int(para_chap)       
                    sent_book = count_sent + int(sent_chap)  
                    word_book = count_word + int(word_chap)
                    
#                     left = re.split('\s|$', left_text[0])   
#                     if left[-1] == '':
#                         left = left[0:len(left)-1]
#                     node = re.split('\s|$', node_text[0]) 
#                     if node[-1] == '':
#                         node = node[0:len(node)-1]
#                     right = re.split('\s|$', right_text[0]) 
#                     if right[-1] == '':
#                         right = right[0:len(right)-1]
#                     conc_line = [re.split('\s|^|$', left_text[0]), re.split('\s|^|$', node_text[0]), re.split('\s|^|$', right_text[0]),
#                                 [book, book_title, chapter, para_chap, sent_chap, word_chap],
#                                 [para_book, sent_book, word_book, total_word]]

                    conc_line = [left_text, node_text, right_text,
                                [book, book_title, chapter, para_chap, sent_chap, str(word_chap)],
                                [str(para_book), str(sent_book), str(word_book), str(total_word)]]
                    
                    
                    conc_lines.append(conc_line)
                    
                if count > 500:
                    break


        conc_lines.insert(0, len(conc_lines))  
        return conc_lines
    
                

                            
            




        
        
        
