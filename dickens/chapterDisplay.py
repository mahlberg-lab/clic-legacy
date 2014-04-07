import os
import re
import timeit

from cheshire3.document import StringDocument
from cheshire3.internal import cheshire3Root
from cheshire3.server import SimpleServer
from cheshire3.baseObjects import Session

from lxml import etree

class ChapterDisplay(object):
    
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
        #self.articleTransformer = self.db.get_object(self.session, 'article-Txr')
        
    def getRS(self, idxName, terms):
        session = self.session
        db = self.db
        qf = self.qf
        
        query = qf.get_query(session, 'c3.%s = "%s"' % (idxName, terms))         
        rs = db.search(session, query)          
               
        return rs

    def articleDisplay(self, idxName, terms):
        session = self.session
         
        rs1 = ChapterDisplay.getRS(self, idxName, terms)
        rec = rs1[0].fetch_record(session) ## chapter 1 in Bleak House
        tree = rec.get_dom(session).getroottree()
        
        print tree.xpath('//div')[0].get('book')
        print rs1[0].proxInfo
        
        search_word = rs1[0].proxInfo[7][0][1] ## occurrence nr 8
        
        all_hits = []
        for m in rs1[0].proxInfo:
            all_hits.append(m[0][1])
            
        matches = [search_word, all_hits]
        
        ## if we want to change
#         for i, word in enumerate(tree.xpath('//div//p//s/descendant::w')):
#             word.tag = 'w.%s' % str(i+1)
            
        #print etree.tostring(tree.xpath('//div/descendant::w[%s+1]' % search_word)[0])
         
        para_list = []    
        for para in tree.xpath('//div//p'):
            wordlist = []
            for i, word in enumerate(para.xpath('.//s/descendant::w')):
                wordlist.append('<w id="%s">%s</w>' % (i+1, word.text))
            para_list.append(wordlist)
 
          
        print para_list[0:2]
         
        #chapterlist = [para_list, matches]
         
        #return chapterlist
 
        #baseXPath = '//*[@eid=EIDVALUE]/following::w[WOFFSET]'
    
    def articleDisplay2(self, idxName, terms):
        
        chapterviewdata = []
        
        extraSpaceElems = ['s']

        session = self.session
         
        rs1 = ChapterDisplay.getRS(self, idxName, terms)
        rec = rs1[0].fetch_record(session) ## chapter 1 in Bleak House
        tree = rec.get_dom(session).getroottree()
        
        print tree.xpath('//div')[0].get('book')
        print rs1[0].proxInfo[0][0][2]
        
#         walker = tree.getiterator()
#         texts = []
#         for c in walker:
#             if c.tag == 'txt':                       
#                 if c.text:
#                     texts.append(c.text)                        
#                 if c.tail:
#                     texts.append(c.tail)
#            
#             ## add space to sentence
#             elif c.tag in extraSpaceElems :
#                 texts.append(' ')
#             else:
#                 continue     
#             
#         text = ''.join(texts).lstrip()
#         chapterviewdata.insert(0, text)
#         print text[rs1[0].proxInfo[0][0][2]:rs1[0].proxInfo[0][0][2]+4]

        sent_list = []    
        for i, para in enumerate(tree.xpath('//div//p//s')):
            sent_list.append(para.xpath('/descendant::txt')[i].text)
            #break
        
        text = ' '.join(sent_list)

        print text[rs1[0].proxInfo[0][0][2]:rs1[0].proxInfo[0][0][2]+4]
        
        chapterviewdata.insert(0, text)
        
         

                
                

        
   

    