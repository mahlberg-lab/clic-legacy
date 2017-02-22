# -*- coding: utf-8 -*-

'''
Build a wordlist of tokens or phrases using the cheshire3
database. 

For instance:

    clusters = Cheshire3WordList()
    clusters.build_wordlist('non-quote-idx', ['ntc'])
    clusters.total
    clusters.wordlist
'''

import copy
import os
import os.path
import pandas as pd

from cheshire3.document import StringDocument
from cheshire3.internal import cheshire3Root
from cheshire3.server import SimpleServer
from cheshire3.baseObjects import Session

BASE_DIR = os.path.dirname(__file__)
CLIC_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))


class Cheshire3WordList(object):
    '''
    Main class used to build Cheshire3 word lists. These
    can be of individual tokens or of clusters (also
    called n-grams or phrases).
    '''

    def __init__(self):
        '''
        Sets up the connection with Cheshire3. 
        '''
        self.session = Session()
        self.session.database = 'db_dickens'
        self.serv = SimpleServer(self.session,
                            os.path.join(CLIC_DIR, 'cheshire3-server', 'configs', 'serverConfig.xml')
                            )
        self.db = self.serv.get_object(self.session, self.session.database)
        self.qf = self.db.get_object(self.session, 'defaultQueryFactory')
        self.idxStore = self.db.get_object(self.session, 'indexStore')
    
    def build_subcorpus_clauses(self, subcorpora):
        '''
        Takes a list of subcorpora and turns it into a 
        CQL query that Cheshire3 can process.
        '''
        
        if not isinstance(subcorpora, list):
            raise IOError, 'subcorpora should be a list'
        
        clauses = []
        for subcorpus in subcorpora:
            if subcorpus in ['dickens', 'ntc']:
                idx = 'subCorpus-idx'
            else:
                idx = 'book-idx'
            clauses.append('c3.{0} = "{1}"'.format(idx, subcorpus))
        return clauses
    
    def get_facets(self, index_name, subcorpora):
        '''
        Get the actual word counts ('facets') using the 
        index and the list of subcorpora. 
        '''
        clauses = self.build_subcorpus_clauses(subcorpora)
        query = self.qf.get_query(self.session,
                                       ' or '.join(clauses)
                                       )
        results = self.db.search(self.session, query)
        idx = self.db.get_object(self.session, index_name)
        facets = idx.facets(self.session, results)
        return facets
        
    def facets_to_df(self, facets):
        '''
        Converts the facets into a dataframe that can be manipulated
        more easily.
        '''
        
        def select_third_value(value):
            '''
            Facets come in the following format:
            [(u'a', (38, 879, 84372)),
             (u'all', (1067, 879, 15104)),
             
            This function returns the third values, respectively 84372 and 15104
            in the example above.
            '''
            return value[2]

        dataframe = pd.DataFrame(facets, columns =['Type', 'Raw facet'])
        dataframe.index += 1
        
        dataframe['Count'] = dataframe['Raw facet'].apply(select_third_value)
        self.total = dataframe.Count.sum() 
        dataframe['Percentage'] = dataframe.Count / self.total * 100
        dataframe['Percentage'] = dataframe['Percentage'].round(decimals=2)
        dataframe.sort_values(by='Count', ascending=False, inplace=True)
        dataframe['Empty'] = ''
        return dataframe
    
    def wordlist_to_json(self):
        '''
        Returns a json string that is 
        adapted to the CLiC API.
        '''
        
        # do not work on the original
        wordlist = copy.deepcopy(self.wordlist)
        del wordlist['Raw facet']
        wordlist = wordlist[['Empty', 'Type', 'Count', 'Percentage']]
        return wordlist.to_json(orient='values')
    
    def build_wordlist(self, index_name, subcorpora):
        '''
        The core method that needs to be called in order to 
        actually generate the keyword list. Once this method is called
        the .wordlist attribute will return the wordlist. 
        '''        
        facets = self.get_facets(index_name, subcorpora)
        self.wordlist = self.facets_to_df(facets)