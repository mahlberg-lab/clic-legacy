import os
import re

from cheshire3.document import StringDocument
from cheshire3.internal import cheshire3Root
from cheshire3.server import SimpleServer
from cheshire3.baseObjects import Session

from lxml import etree

import json

booklist_r = open('/home/aezros/clic/dickens/booklist', 'r')
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
       
    def create_concordance(self, terms, idxName, wordWindow, Materials, selectWords): 
        ## create a list of lists containing each three contexts, and a list within those contexts containing each word
        session = self.session
        db = self.db
        qf = self.qf
        
        extraSpaceElems = ['s']
        conc_lines = []
        
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
            terms = [terms]  
        else:
            terms = terms.split(' ')
        
        term_clauses = []
        for term in terms:
            term_clauses.append('c3.{0} = "{1}"'.format(idxName, term))
        
        print term_clauses
        
        ## /proxInfo needed to search individual books
        #query = qf.get_query(session, ' or '.join(books) + ' and/proxInfo ' + 'c3.%s = "%s"' % (idxName, terms)) 
        query = qf.get_query(session, ' or '.join(books) + ' and/proxInfo ' + ' or '.join(term_clauses))         
        rs = db.search(session, query)  
    
        if len(rs) > 0:
            count = 0
            temp = []
            for i in rs:
                
                rec = i.fetch_record(session)
                tree = rec.get_dom(session).getroottree()           
               
                for m in i.proxInfo: 
                    count += 1
                    
                    if idxName in ['chapter-idx']:     
                        elems = [0]      
                        (e, w) = (0, m[0][1])                                           
               
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
                        (e, w) = (0, w) 
                        
                    ## sentences etc.                      
                    else:
                        temp.append(m[0][0])
                        elems = set(temp)
                        (e, w) = (m[0][0], m[0][1]) 
                    
                    ## get indexes
                    if idxName in ['quote-idx', 'non-quote-idx', 'longsus-idx', 'shortsus-idx']: 
                        index = db.get_object(session, 'chapter-idx')                 
                    else:
                        index = db.get_object(session, '%s' % (idxName))
                        
                    vecs = {}  
                    for el in elems:
                        vecs[el] = self.idxStore.fetch_proxVector(session, index, i, e)   
                    v = vecs[el] 
                    
                    nodeLength = len(m)            
                
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
                            
                    ## string location
                    wordWindow = int(wordWindow)
                    leftOnset = v[max(0, w-(wordWindow+1))][2]
                    leftOffset = v[w][2]
                    nodeOffset = v[min(w+nodeLength, len(v)-1)][2]
                    rightOffset = v[min(w+nodeLength+wordWindow, len(v)-1)][2]
#                     finalOffset = finalOffset

                    
                    proxOffset = [leftOnset, leftOffset, nodeOffset, rightOffset]

                    if idxName in ['sentence-idx']:
                        tree = tree.xpath('//*[@eid=%s]' % i.proxInfo[0][0][0])[0]
                    else:
                        tree
                     
                    walker = tree.getiterator()
                    texts = []
                    for c in walker:
                        if c.tag == 'txt':                       
                            if c.text:
                                texts.append(c.text)                        
                            if c.tail:
                                texts.append(c.tail)
                       
                        ## add space to sentence
                        elif c.tag in extraSpaceElems :
                            texts.append(' ')
                        else:
                            continue     
                      
                    text = ''.join(texts).lstrip()
                    left_text = [text[proxOffset[0]:proxOffset[1]]]
                    node_text = [text[proxOffset[1]:proxOffset[2]]]
                    #print node_text
                    right_text = [text[proxOffset[2]:proxOffset[3]]]

                    #conc_line = [re.split('\s|^|$', left_text[0]), re.split('\s|^|$', node_text[0]), re.split('\s|^|$', right_text[0])]
                    
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
                    for b in booklist:
                        if b[0][0] == book:
          
                            for j, c in enumerate(b[2]):
                                while j+1 < int(chapter):
                                    count_para = count_para + int(c[0])
                                    count_sent = count_sent + int(c[1])
                                    count_word = count_word + int(c[2])
                                    j += 1
                                    break
                              
                    para_book = count_para + int(para_chap)       
                    sent_book = count_sent + int(sent_chap)  
                    word_book = count_word + int(word_chap)    

                    conc_line = [re.split('\s|^|$', left_text[0]), re.split('\s|^|$', node_text[0]), re.split('\s|^|$', right_text[0]),
                                [book, chapter, para_chap, sent_chap, word_chap],
                                [para_book, sent_book, word_book]]
                     
                    conc_lines.append(conc_line)
                    
                if count > 200:
                    break

        conc_lines.insert(0, len(conc_lines))  
        return conc_lines
                

                            
            




        
        
        
