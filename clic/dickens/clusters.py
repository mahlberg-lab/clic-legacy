import os
import re
from math import log1p

from cheshire3.document import StringDocument
from cheshire3.internal import cheshire3Root
from cheshire3.server import SimpleServer
from cheshire.baseObjects import Session

cheshirePath = os.path.join('HOME', '/home/cheshire')

class Clusters(object):
    
    def __init__(self):
        self.session = Session()
        self.session.database = 'db_dickens'
        self.serv = SimpleServer(self.session,
                            os.path.join(cheshire3Root, 'configs', 'serverConfig.xml')
                            )
        self.db = serv.get_object(self.session, self.session.database)
        self.qf = self.db.get_object(self.session, 'defaultQueryFactory')
        self.resultSetStore = self.db.get_object(self.session, 'resultSetStore')        
        self.idxStore = self.db.get_object(self.session, 'indexStore')
        self.logger = self.db.get_object(self.session, 'clusterLogger') ## add to dbs/dickens/config
        
    def list_clusters(self, IdxName, Materials):
        #self.logger.log('CREATING CLUSTERS FOR RS: {0}'.format(id)) 
        session = self.session
        db = self.db
        
        