import os
import re

from cheshire3.document import StringDocument
from cheshire3.internal import cheshire3Root
from cheshire3.server import SimpleServer
from cheshire3.baseObjects import Session

from lxml import etree

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
        
#     def search(self, req):        
#         ## get search id and identify the relevant records
#         args = request.args
        
    def create_concordance(self, terms, idxName, wordWindow): #, Materials): 
        ## create a list of lists containing each three contexts, and a list within those contexts containing each word
        session = self.session
        db = self.db
        qf = self.qf
        
        extraSpaceElems = ['s']
        conc_lines = []
        
        query = qf.get_query(session, 'c3.%s = "%s"' % (idxName, terms))
        rs = db.search(session, query)   
    
        if len(rs) > 0:
            temp = []
            for i in rs:
                rec = i.fetch_record(session)
                tree = rec.get_dom(session).getroottree()           
               
                for m in i.proxInfo: 
                    
                    if idxName in ['chapter']:     
                        elems = [0]      
                        (e, w) = (0, m[0][1])   
                        print w                
               
                    elif idxName in ['quote', 'non-quote', 'longsus', 'shortsus']:  
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
                    if idxName in ['quote', 'non-quote', 'longsus', 'shortsus']: 
                        index = db.get_object(session, 'chapter-idx')                 
                    else:
                        index = db.get_object(session, '%s-idx' % (idxName))
                        
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
                    leftOnset = v[max(0, w-(wordWindow+1))][2]
                    leftOffset = v[w][2]
                    nodeOffset = v[min(w+nodeLength, len(v)-1)][2]
                    rightOffset = v[min(w+nodeLength+wordWindow, len(v)-1)][2]
#                     finalOffset = finalOffset

                    
                    proxOffset = [leftOnset, leftOffset, nodeOffset, rightOffset]

                    if idxName in ['sentence']:
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
                    print node_text
                    right_text = [text[proxOffset[2]:proxOffset[3]]]

                    conc_line = [re.split('\s|^|$', left_text[0]), re.split('\s|^|$', node_text[0]), re.split('\s|^|$', right_text[0])]
                     
                    conc_lines.append(conc_line)
             
        return conc_lines
                

                            
            




        
        
        
