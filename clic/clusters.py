# -*- coding: utf-8 -*-

'''
Tool to create wordlists based on the entries in an index.
'''

import os
import operator

from cheshire3.document import StringDocument
from cheshire3.internal import cheshire3Root
from cheshire3.server import SimpleServer
from cheshire3.baseObjects import Session

cheshirePath = os.path.join('HOME', '/home/cheshire')

class Clusters(object):
    '''
    Class that does all the heavy weighting. It makes the connection with
    cheshire3, uses the input parameters (indexname and subcorpus/Materials) to
    return a list of words and their total number of occurrences.

    For instance,


        the 98021
        to  78465
        ...

    or
        he said  8937
        she said 6732
        ...

    '''

    def __init__(self):
        '''
        Set up the connection to cheshire3.
        '''
        self.session = Session()
        self.session.database = 'db_dickens'
        self.serv = SimpleServer(self.session,
                            os.path.join(cheshire3Root, 'configs', 'serverConfig.xml')
                            )
        self.db = self.serv.get_object(self.session, self.session.database)
        self.qf = self.db.get_object(self.session, 'defaultQueryFactory')
        self.resultSetStore = self.db.get_object(self.session, 'resultSetStore')
        self.idxStore = self.db.get_object(self.session, 'indexStore')
        self.logger = self.db.get_object(self.session, 'clusterLogger') ## added to dbs/dickens/config.xml

    def list_clusters(self, idxName, Materials):
        '''
        Build a list of clusters and their occurrences.

        Limit the list to the first 3000 entries.
        '''

        #self.logger.log(10, 'CREATING CLUSTERS FOR RS: {0} in {1}'.format(idxName, Materials))
        session = self.session
        db = self.db

        clauses = []
        for Material in Materials:
            if Material in ['dickens', 'ntc']:
                MatIdx = 'subCorpus-idx'
            else:
                MatIdx = 'book-idx'
            clauses.append('c3.{0} = "{1}"'.format(MatIdx, Material))

        query = self.qf.get_query(session,
                                       ' or '.join(clauses)
                                       )
        results = db.search(session, query)

        idx = db.get_object(session, idxName)
        facets = idx.facets(session, results)
        dict = {}
        for x in facets:
            dict[x[0]] = x[1][2]

        cluster_list = []
        for term, freq in dict.iteritems():
            if freq >= 2:
                prop = (float(freq)/float(len(dict))) * 100
                cluster_list.append(['', term, freq, str(prop)[:5]])  ## add empty array node at beginning (see Pete email 23.04.14)

        cluster_list.sort(key=operator.itemgetter(2), reverse=True)

        if len(cluster_list) <= 3001:
            return cluster_list
        else:
            return cluster_list[0:3000]
