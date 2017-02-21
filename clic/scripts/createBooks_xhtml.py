import os
import re

from cheshire3.document import StringDocument
from cheshire3.internal import cheshire3Root
from cheshire3.server import SimpleServer
from cheshire3.baseObjects import Session

from lxml import etree

class Chapter_view(object):
    
    def __init__(self):
        self.session = Session()
        self.session.database = 'db_dickens'
        self.serv = SimpleServer(self.session, 
                                 os.path.join(cheshire3Root, 'configs', 'serverConfig.xml')
                                 )
        self.db = self.serv.get_object(self.session, self.session.database)
        self.qf = self.db.get_object(self.session, 'defaultQueryFactory')
        self.idxStore = self.db.get_object(self.session, 'indexStore')
        
    def search_book(self, book):
        session = self.session
        db = self.db
        qf = self.qf        
       
        book_query = qf.get_query(session, 'c3.book-idx = "%s"' % book)
        book_results = db.search(session, book_query)
        return book_results
        

    def create_chapterXhtml(self, book_results):
        session = self.session    

        book = self.search_book(book_results)        
        
        #chapter_list = [] ## one list per chapter
        chapter_dict = {}
        for ch in book:
            
            rec = ch.fetch_record(session)
            tree = rec.get_dom(session).getroottree()  
            #print etree.tostring(tree)
            title = tree.xpath('//div//title')[0].text ## for html page
            ch_number = tree.xpath('//div')[0].get('num')  ## for filename  
            
            countwords = 0           
            paralist = [] ## para
            for para in tree.xpath('//div//p'):             
                paralist.append('<p>')
                   
                spanlist = []
                for i, w in enumerate(para.xpath('./descendant::w')):
                    countwords += 1
                    try: ## only if there is preceding n
                        ## only print n if not empty (as we add space outside the spans - see *)
                        if not re.match('[^\s$]|[\W|^--$]', w.xpath('./preceding-sibling::n[1]')[0].text): 
                            preceding_n = w.xpath('./preceding-sibling::n[1]')[0].text
                        else:
                            preceding_n = ''
                    except:
                        preceding_n = ''
                    ## only print n if not empty (as we add space outside the spans - see *)
                    try: ## only if there is following n
                        if not w.xpath('./following-sibling::n[1]')[0].text == ' ':
                            following_n = w.xpath('./following-sibling::n[1]')[0].text
                        else: 
                            following_n = ''
                    except:
                        following_n = ''
                    word = preceding_n + w.text + following_n
                        
                    spanlist.append('<span id="%s">%s</span>' % (countwords, word))
 
                spans = ' '.join(spanlist) ## * 
                spans = re.sub('--', ' --', spans)
             
                paralist.append(spans)
                paralist.append('</p>')
              
            paras = ''.join(paralist)
            chapter = ''.join('<!DOCTYPE html>' + '\n' + 'html lang="en">' + '\n' +
                              '<head>' + '\n' +
                              'meta charset="utf-8">' + '\n' +
                              '<title>' + title + '</title>' + '\n'
                              '</head>' + '\n\n' +
                              '<body>' + '\n\n' +
                               paras + '\n\n' +
                               '</body>' + '\n\n' +
                               '</html>')
            
            chapter_dict[chapter] = ch_number
            print tree.xpath('//div')[0].get('book'), ch_number
            #break
            
        return chapter_dict
            





            

        


        