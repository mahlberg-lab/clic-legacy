import os
import re
from math import log1p

from cheshire3.document import StringDocument
from cheshire3.internal import cheshire3Root
from cheshire3.server import SimpleServer
from cheshire3.baseObjects import Session

cheshirePath = os.path.join('HOME', '/home/cheshire')

class Clusters(object):
    
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
        self.logger = self.db.get_object(self.session, 'clusterLogger') ## add to dbs/dickens/config
        
    def list_clusters(self, idxName, Materials):
        #self.logger.log('CREATING CLUSTERS FOR RS: {0}'.format(id)) 
        #self.logger.log(10, '%s\t%s' % (idxName + ' '.join(Materials)))
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
            cluster_list.append([term, freq])
            
        return cluster_list