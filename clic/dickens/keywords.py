### THIS IS A SKETCH

import os
import re
from math import log1p
import operator

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
        self.logger = self.db.get_object(self.session, 'keywordLogger')
        
    def list_keywords(self, testIdxName, testMaterials, refIdxName, refMaterials, pValue):
        #self.logger.log(10, 'CREATING KEYWORDS FOR RS: {0} in {1}, compared to {2} in {3}'.format(testIdxName, testMaterials, refIdxName, refMaterials)) 
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
                    LL = '%.2f' % LL
                except:
                    LL = 909090
            else:
                try:
                    LL = -2*((freqTest*log1p(freqTest/expectedTest)) + (freqRef*log1p(freqRef/expectedRef)))
                    LL = '%.2f' % LL
                except:
                    LL = 909090
            
            if freqRef == 5.0e-324:
                freqRef2 = 0
            else:
                freqRef2 = int('%.0f' % freqRef)               
       
           
            dec_Test = '%.2f' % freqTest
            dec_Ref = '%.2f' % freqRef
            #propTest = (float(dec_Test)/354362) * 10000 (normalised per 10000)
            #propRef = (float(dec_Ref)/354362) * 10000  
            propTest = (float(dec_Test)/testLength) * 100
            propRef = (float(dec_Ref)/refLength) * 100
           

            if float(pValue) <= 0.000001: ## not dealing with smaller p values as yet
                if float(LL) >= 23.92:# or float(LL) <= -23.92:
                    kw_list.append(['', term, str(freqTest), '%.2f' % propTest, str(freqRef2), '%.2f' % propRef, float(LL), pValue])
                      
            else:
                if float(pValue) == 0.00001:
                    if (float(LL) > 19.59):# or (float(LL) < -19.59):
                        kw_list.append(['', term, str(freqTest), '%.2f' % propTest, str(freqRef2), '%.2f' % propRef, float(LL), pValue])    
                elif float(pValue) == 0.0001: 
                    if (float(LL) > 15.13):# or (float(LL) < -15.13):
                        kw_list.append(['', term, str(freqTest), '%.2f' % propTest, str(freqRef2), '%.2f' % propRef, float(LL), pValue])  
                elif float(pValue) == 0.001: 
                    if (float(LL) > 10.83):# or (float(LL) < -10.83):
                        kw_list.append(['', term, str(freqTest), '%.2f' % propTest, str(freqRef2), '%.2f' % propRef, float(LL), pValue]) 
                elif float(pValue) == 0.01: 
                    if (float(LL) > 6.63):# or (float(LL) < -6.63):
                        kw_list.append(['', term, str(freqTest), '%.2f' % propTest, str(freqRef2), '%.2f' % propRef, float(LL), pValue]) 
                elif float(pValue) == 0.05: 
                    if (float(LL) > 3.84):# or (float(LL) < -3.84):
                        kw_list.append(['', term, str(freqTest), '%.2f' % propTest, str(freqRef2), '%.2f' % propRef, float(LL), pValue]) 
                elif float(pValue) == 0.1: ## NB: returns all values
                    if (float(LL) > 2.71):# or (float(LL) < -2.71):
                        kw_list.append(['', term, str(freqTest), '%.2f' % propTest, str(freqRef2), '%.2f' % propRef, float(LL), pValue]) 

        kw_list.sort(key=operator.itemgetter(6), reverse=True) ## reverse for descending order
        
        #return kw_list[0:1500] ## NB: Interface doesn't return first list item
        return kw_list[0:4999]

                                            
        
        
        
        