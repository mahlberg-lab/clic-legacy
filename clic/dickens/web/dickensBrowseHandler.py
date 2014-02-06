
import cgitb
import os
import re
import smtplib
import sys
import time
import traceback
import urllib

# import mod_python stuffs
from mod_python import apache, Cookie
from mod_python.util import FieldStorage

from cheshire3.internal import cheshire3Root

databaseName = 'dickens'
cheshirePath = os.environ.get('HOME', '/home/cheshire')

# value to normalize frequency counts by
normalizationBase = 10000
z = False
zstatSig = 3
tfp = False

# settings
browseIndexes = ['sentence-idx', 'quote-idx', 'non-quote-idx', 'shortsus-idx', 'longsus-idx', '3gram-idx', 'non-quote-3gram-idx', 'quote-3gram-idx', '4gram-idx', 'non-quote-4gram-idx', 'quote-4gram-idx', '5gram-idx', 'non-quote-5gram-idx', 'quote-5gram-idx', 'longsus-5gram-idx']
indexForStats = 'sentence-idx'

# import Cheshire3/PyZ3950 stuff
from cheshire3.baseObjects import Session
from cheshire3.document import StringDocument
import cheshire3.exceptions
from cheshire3.internal import cheshire3Root
from cheshire3.server import SimpleServer

from clic.stats import zscore

# C3 web search utils

class BrowseHandler(object):

    htmlPath = os.path.join(cheshirePath, 'clic', 'www', databaseName, 'html')
    logger = None
    redirected = False

    def __init__(self, lgr):
        self.logger = lgr
        build_architecture()

    def send_html(self, data, req, code=200):
        req.content_type = 'text/html'
        req.content_length = len(data)
        if (type(data) == unicode):
            data = data.encode('utf-8')
        req.write(data)
        req.flush()    

    def send_xml(self, data, req, code=200):
        req.content_type = 'text/xml'
        req.content_length = len(data)
        if (type(data) == unicode):
            data = data.encode('utf-8')
        req.write(data)
        req.flush()   

    def comma(self, d):
        s = str(d)
        if s.find('.') != -1:
            a = s[:s.find('.')]
            b = s[s.find('.'):]
        else:
            a = s
            b = ''
        l = []
        while len(a) > 3:
            l.insert(0, a[-3:])
            a = a[0:-3]
        if a:
            l.insert(0, a)
        return ','.join(l) + b

    def create_TFP(self, form):
        word = form.get('word', None)
        indexName = form.get('index', None)
        if indexName != 'sentence':
            cql = 'c3.sentence-idx exact %s' % word
            q = qf.get_query(session, cql)
            rs_base = db.search(session,q)
            
            cql = 'c3.%s-idx exact %s' % (indexName, word)
            q = qf.get_query(session, cql)
            rs = db.search(session, q)
            subset = []
            hits = len(rs)
            if (hits > 0):
                for r in rs:
                    subset.append(r)

            hits_base = len(rs_base)
            dist_base = {}
            dist_pos = {}
            dist_neg = {}
            if (hits_base > 0):
                for r in rs_base:
                    try:
                        dist_base[r.occurences] += 1
                    except:
                        dist_base[r.occurences] = 1
                    if r in subset:
                        try:
                            dist_pos[r.occurences] += 1
                        except:
                            dist_pos[r.occurences] = 1
                    else:
                        try:
                            dist_neg[r.occurences] += 1
                        except:
                            dist_neg[r.occurences] = 1
                            
            hits_base = sum(dist_base.values())
            hits_pos = sum(dist_pos.values())
            hits_neg = sum(dist_neg.values())
            
            output = ['<table><tr><td>frequency</td><td>when in %s (%s)</td><td>when not in %s (%s)</td><td>all</td></tr>' % (indexName, '%', indexName, '%')]
            for i in [1, 2, 3]: 
                output.append('<tr><td>%s</td><td>%0.2f</td><td>%0.2f</td><td>%0.2f</td></tr>' % (i, max(float(dist_pos[i])/float(hits_pos) * 100.0,0), max(float(dist_neg[i])/float(hits_neg) * 100.0,0), max(float(dist_base[i])/float(hits_base) * 100.0,0)))  
            fourPlus_base = 0
            fourPlus_pos = 0
            fourPlus_neg = 0
            for i in range(4,max(dist_base.keys())):
                try:
                    fourPlus_base += dist_base[i]
                except:
                    continue
            for i in range(4,max(dist_pos.keys())):
                try:
                    fourPlus_pos += dist_pos[i]
                except:
                    continue
            for i in range(4,max(dist_neg.keys())):
                try:
                    fourPlus_neg += dist_neg[i]
                except:
                    continue
            output.append('<tr><td>4+</td><td>%0.2f</td><td>%0.2f</td><td>%0.2f</td></tr>' % (max(float(fourPlus_pos)/float(hits_pos) * 100.0,0), max(float(fourPlus_neg)/float(hits_neg) * 100.0,0), max(float(fourPlus_base)/float(hits_base) * 100.0,0)))
            output.append('</table>')
            return ''.join(output)    
        else :
            dist = {}
            cql = 'c3.%s-idx exact %s' % (indexName, word)
            q = qf.get_query(session, cql)
            rs = db.search(session,q)
            hits = len(rs)
            if (hits>0):
                for r in rs:
                    try:
                        dist[r.occurences]+=1
                    except:
                        dist[r.occurences]=1
            hits = sum(dist.values())
            output = ['<table><tr><td>frequency</td><td>total articles</td><td>%</td></tr>']
        
            for i in [1,2,3]:
                try :
                    output.append('<tr><td>%s</td><td>%s</td><td>%0.2f</td></tr>' % (i, dist[i], float(dist[i])/float(hits) * 100.0))  
                except KeyError :
                    output.append('<tr><td>%s</td><td>0</td><td>0</td></tr>' % i)
            fourPlus=0
            for i in range(4,max(dist.keys())):
                try:
                    fourPlus += dist[i]
                except:
                    continue
            try :
                output.append('<tr><td>4+</td><td>%s</td><td>%0.2f</td></tr>' % (fourPlus, float(fourPlus)/float(hits) * 100.0))
            except KeyError:
                output.append('<tr><td>4+</td><td>0</td><td>0</td></tr>')
            output.append('</table>')
            return ''.join(output)
            #print "\n%i occurrences in %i articles" % (occs,hits)    
    
    # TODO: firstTotal and total need to be generated from the equivalent non-gram index nOccs    
    def compareIndexes(self, req):
        self.logger.log('comparing indexes')
        start = time.time()
        form = FieldStorage(req)
        id = form.get('id','data_grid')
        offset = str(form.get('offset', 0))
        if offset.find('.') != -1:
            startNum = int(offset[:offset.find('.')])
            adjustValue = int(offset[offset.find('.')+1:])
        else :
            startNum = int(offset)
            adjustValue = 0       
        howMany = int(form.get('page_size', 100))
        indexStrings = form.get('index', None)
        baseIdx = db.get_object(session, indexForStats)
        corpusSize = baseIdx.fetch_metadata(session)['nOccs']
        indexList = []
        addTfp = False
        # list means we are comparing indexes otherwise its just one
        # we get the actual index object from the string and store them in indexList
        if (indexStrings.__class__ == list):
            if (indexStrings[0].find('gram') == -1):
                addTfp = True
            for i in range(0, len(indexStrings)):
                if indexStrings[i].find('gram') == -1:
                    compareIndex = db.get_object(session, '%s' % indexStrings[i])
                else: 
                    if indexStrings[i].replace('-idx', '').find('-') == -1:
                        compareIndex = db.get_object(session, 'sentence-idx')
                    else:                   
                        compareIndex = db.get_object(session, '%s-idx' % indexStrings[i][:indexStrings[i].replace('-idx', '').rfind('-')])
                indexList.append((db.get_object(session, '%s' % indexStrings[i]), compareIndex))  
        else :
            if (indexStrings.find('gram') == -1):
                addTfp = True
                compareIndex = db.get_object(session, '%s' % indexStrings)
            else:
                if indexStrings.replace('-idx', '').find('-') == -1:
                    compareIndex = db.get_object(session, 'sentence-idx')
                else:
                    compareIndex = db.get_object(session, '%s-idx' % indexStrings[:indexStrings.replace('-idx', '').rfind('-')])
            indexList.append((db.get_object(session, '%s' % indexStrings), compareIndex))  

#            indexList.append(db.get_object(session, '%s' % indexStrings))
        # 
        output = []
        firstIndex = indexList[0][0]
        
        firstTotal = indexList[0][1].fetch_metadata(session)['nOccs']
        q = qf.get_query(session, 'idx-foo any "bar"')
        appending = True
        if startNum < 0 :
            appending = False
            startNum = startNum/-1
        
        idxLength = firstIndex.fetch_metadata(session)['nTerms']
        completed = False
        cycles = 0
        firstStart = startNum
        while len(output) < howMany and completed == False:     
            if appending:
                startNum = int(firstStart+(howMany*cycles))
            else:
                startNum = int(startNum-(howMany*cycles))
            cycles += 1
            if appending and idxLength-(startNum) <= howMany:
                completed = True
            if appending:
                termList = firstIndex.fetch_termFrequencies(session, 'occ', startNum, min(howMany, idxLength-(startNum)), '>')
            else:
                termList = firstIndex.fetch_termFrequencies(session, 'occ', startNum, min(howMany, startNum), '<')         
            for i, t in enumerate(termList):                
                cells = []
                word = firstIndex.fetch_termById(session, t[1])
                q.term.value = word
                percentage = round((float(t[2]) / float(firstTotal) * normalizationBase), 2)
                firstIndexName = indexList[0][0].id[:indexList[0][0].id.find('-idx')]
                
                if appending:
                    cells.append('<td>%d</td>' % (i + 1 + startNum))
                else:                   
                    cells.append('<td>%d</td>' % (startNum + 1 - i))
                # This try/except/else deals with whether we are viewing one
                # index or more than one
                try:
                    indexList[1]
                except:
                    # A single index     
                    if addTfp == True and tfp == True:                                       
                        cells.append('<td><a href="javascript:searchFor(\'%s\', \'%s\')">%s</a></td><td><a href="javascript:tfpFor(\'%s\', \'%s\')">tfp</a></td><td>%s</td>' % (word, firstIndexName, word, word, firstIndexName, percentage))                     
                    else :
                        cells.append('<td><a href="javascript:searchFor(\'%s\', \'%s\')">%s</a></td><td>%s</td>' % (word, firstIndexName, word, percentage))                     
                    cells.append('<td>%s</td>' % t[2])     
                # more than one index
                else:                    
                    if addTfp == True and tfp == True:
                        cells.append('<td>&lt;a href="javascript:searchFor(\'%s\', \'%s\')">%s&lt;/a></td><td>&lt;a href="javascript:tfpFor(\'%s\', \'%s\')">tfp&lt;/a></td><td>%s</td>' % (word, firstIndexName, word, word, firstIndexName, percentage))                     
                    else :
                        cells.append('<td>&lt;a href="javascript:searchFor(\'%s\', \'%s\')">%s&lt;/a></td><td>%s</td>' % (word, firstIndexName, word, percentage))                     
                    othersTotal = 0
                    othersHits = 0 
                    self.logger.log(cells)              
                    for j in range(1, len(indexList)):
                        total = indexList[j][1].fetch_metadata(session)['nOccs']
                        othersTotal += total
                        occs = indexList[j][0].scan(session, q, 1)    
                        
                        if (occs[0][0] == word):
                            othersHits += occs[0][1][2]
                            #add each cell
                            normalisedOccs = round((float(occs[0][1][2]) / float(total) * normalizationBase), 2)
                            cells.append('<td>%s</td>' % normalisedOccs)
                        else :
                            cells.append('<td>0</td>')                        
                    if z :
                        zstat = zscore(othersHits, t[2], othersTotal, indexList[0][1].fetch_metadata(session)['nOccs'])
                        if zstat >= zstatSig:
                            cells.append('<td>%s</td>' % zstat)
                        else :
                            continue      
                output.append('<tr>%s</tr>' % ''.join(cells))

            if not appending:
                output.reverse()
           # output = output[adjustValue:]
        (mins, secs) = divmod(time.time()-start, 60)
        self.logger.log('scanning complete: %s' % secs) 
        return '<ajax-response><response type="object" id="%s_updater"><rows update_ui="true">%s</rows></response></ajax-response>' % (id, ''.join(output))

    def sortFunc (self, x, y):       
        return cmp(self.getNum(x),self.getNum(y))       

    def getNum(self, str): 
        try : 
            return int(re.findall(r'\d+', str)[0])
        except :
            return 0

    def getIndexList(self, req):
        indexStore = db.get_object(session, 'indexStore')
        output = []
        for i in indexStore :
            if i.id in browseIndexes:
                output.append('<option class="%s" value="%s">%s</option>' % (self.getNum(i.id), i.id, i.id[:-4]))
        output.sort()
        output.sort(self.sortFunc)
        return '<xml>%s</xml>' % ''.join(output)

    def getStatsTable(self, req):
        indexList = ['sentence-idx', 'quote-idx', 'non-quote-idx', 'shortsus-idx', 'longsus-idx']
        output = ['<tr><th>Sub-Corpus</th><th>Total Word Count</th></tr>']
        for string in indexList:
            index = db.get_object(session, string)
            md = index.fetch_metadata(session)
            output.append('<tr><td>%s</td><td class="number">%s</td></tr>' % (string[:string.rfind('-')], self.comma(md['nOccs'])))        
        return '<xml>%s</xml>' % ''.join(output)
   

    def handle(self, req):
        form = FieldStorage(req)
        mode = form.get('mode', None)
        if (mode == 'compare'):
            page = self.compareIndexes(req)
            self.send_xml(page, req)
        elif (mode == 'index') :
            page = self.getIndexList(req)
            self.send_xml(page, req)
        elif (mode == 'statstable') :
            page = self.getStatsTable(req)
            self.send_xml(page, req)
        elif (mode == 'tfp') :
            page = self.create_TFP(form)
            self.send_xml(page, req)
       

def build_architecture(data=None):
    global session, serv, db, qf, xmlp, recordStore, sentenceStore, paragraphStore, resultSetStore, articleTransformer, kwicTransformer
    session = Session()
    session.environment = 'apache'
    session.user = None
    serv = SimpleServer(session,
                        os.path.join(cheshire3Root, 'configs', 'serverConfig.xml')
                        )
    
    session.database = 'db_' + databaseName
    db = serv.get_object(session, session.database)
    qf = db.get_object(session, 'defaultQueryFactory')
    xmlp = db.get_object(session, 'LxmlParser')
    recordStore = db.get_object(session, 'recordStore')
    articleTransformer = db.get_object(session, 'article-Txr')
    kwicTransformer = db.get_object(session, 'kwic-Txr')

