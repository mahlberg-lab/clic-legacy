### THIS IS A SKETCH

import os
import re
from math import log1p

from cheshire3.document import StringDocument
from cheshire3.internal import cheshire3Root
from cheshire3.server import SimpleServer
from cheshire3.baseObjects import Session

cheshirePath = os.path.join('HOME', '/home/cheshire')

class Keywords(object):
    
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
        #self.logger = self.db.get_object(self.session, 'keywordLogger')
        
    def list_keywords(self, testIdxName, testMaterials, refIdxName, refMaterials):
        #self.logger.log(10, 'CREATING KEYWORDS FOR RS: {0}'.format(id)) 
        #self.logger.log(10, ' '.join(testIdxName + testMaterials[0] + refIdxName + refMaterials[0]))
        session = self.session
        db = self.db

        # Test results
        clauses = []
        for testMaterial in testMaterials:
            if testMaterial in ['dickens', 'ntc']:
                testMatIdx = 'subCorpus-idx'
            else:
                testMatIdx = 'book-idx'
            clauses.append('c3.{0} = "{1}"'.format(testMatIdx, testMaterial))
            
        #return ' or '.join(clauses)

        test_query = self.qf.get_query(session,
                                       ' or '.join(clauses)
                                       )        
        test_results = db.search(session, test_query)
        #return len(test_results) ###
        test_idx = db.get_object(session, testIdxName)
        test_facets = test_idx.facets(session, test_results)
        #return len(test_facets) ###
        ## create dictionary containing word/cluster and number of occurrences
        #test_dict = {x[0]: x[1][2] for x in test_facets}
        test_dict = {}
        for x in test_facets:
            test_dict[x[0]] = x[1][2]        
        
        # [("term", (termId, totalRecords, totalOccurrences)), ("tern2", (...))]
        # Reference results
        clauses_ref = []
        for refMaterial in refMaterials:
            if refMaterial in ['dickens', 'ntc']:
                refMatIdx = 'subCorpus-idx'
            else:
                refMatIdx = 'book-idx'
            clauses_ref.append('c3.{0} = "{1}"'.format(refMatIdx, refMaterial))

        ref_query = self.qf.get_query(session,
                                       ' or '.join(clauses_ref)
                                       )
        ref_results = db.search(session, ref_query)
        ref_idx = db.get_object(session, refIdxName)
        ref_facets = ref_idx.facets(session, ref_results)
        #ref_dict = {x[0]: x[1][2] for x in ref_facets}
        ref_dict = {}
        for x in ref_facets:
            ref_dict[x[0]] = x[1][2]
        
        ## get test length
        testLength = sum(test_dict.values())
        refLength = sum(ref_dict.values())
# 
#         refLength = 0
#         for i in referenceIndex:
#             refLength += i.totalOccs
#         ## refLength is the difference between reference and test
#         refLength = refLength - testLength

#         KW_list = ""
#         for i in testIndex:
#             freqTest = i.totalOccs
#             q = qf.get_query(session, 'c3.%s-idx = "%s"' % (idx, i.queryTerm))
#             ## search for query in sentences
#             ## (not sure what 1, = does)
#             ref = referenceIndex.scan(session, q, 1, '=')
#             if len(ref):
#                 ## We want to know how many observations of a given word is found in ref corpus but not in test corpus
#                 ## Subtract number of occurrences in testIndex from number of occurrences in sentences
#                 freqRef = float(ref[0][1][2] - freqTest)
#                 if freqRef <= 0:
#                     freqRef = 5.0e-324 
#             else:
#                 freqRef = 5.0e-324
        
        kw_list = []
        for term, freqTest in test_dict.iteritems():
            try:
                ## We want to know how many observations of a given word is found in ref corpus but not in test corpus
                ## Subtract number of occurrences in testIndex from number of occurrences in sentences
                freqRef = float(ref_dict[term] - freqTest)
            except KeyError:
                freqRef = 5.0e-324
            else:
                if freqRef <= 0:
                    freqRef = 5.0e-324
            
            ## following Paul Ryson formula for log likelihood (http://ucrel.lancs.ac.uk/llwizard.html)
            ## 1. Expected occurrence within corpus
            ## 1a. Expected reference value: based on sentence index
            ## - Get the total N from corpus 1 (reference corpus)
            ## - Multiply by the sum of observations only found in corpus 1 and those only found in corpus 2 (test corpus)
            ## - Divide by the sum of total N in test corpus and reference corpus
            expectedRef = refLength*(freqTest+freqRef)/(testLength+refLength)
            ## 1b. Expected test value: based on quotes index
            ## Equivalent steps to 1a, but multiply by test N
            expectedTest = testLength*(freqTest+freqRef)/(testLength+refLength)
              
            ## 2. Log Likelihood
            ## Compare actual observations with expected ocurrence for both test and ref, and add these values
            ## Use log1p() (for natural logarithm - ln) instead of log()
            if freqTest*log1p(freqTest/expectedTest) >= freqRef*log1p(freqRef/expectedRef):
                try:
                    LL = 2*((freqTest*log1p(freqTest/expectedTest)) + (freqRef*log1p(freqRef/expectedRef)))
                    LL = '%.3f' % LL
                except:
                    LL = 909090
            else:
                try:
                    LL = -2*((freqTest*log1p(freqTest/expectedTest)) + (freqRef*log1p(freqRef/expectedRef)))
                    LL = '%.3f' % LL
                except:
                    LL = 909090
            
            if freqRef == 5.0e-324:
                freqRef2 = 0
            else:
                freqRef2 = freqRef
                
            if LL > 15.13 or LL < -15.13:
                p_value = 0.0001
            else:
                p_value = 0.001
            
            ## only print if occurence > 3
            if freqTest > 3 and p_value == 0.0001:
                kw_list.append([term, freqTest, freqRef2, LL, p_value])

        return kw_list
                                            
        
        
        
        