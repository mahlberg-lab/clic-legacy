#!/bin/env python

import getpass
import os
import sys
import traceback

from lxml import etree
from crypt import crypt

import cheshire3

from cheshire3.baseObjects import Session
from cheshire3.server import SimpleServer
from cheshire3.internal import cheshire3Root
from cheshire3.document import StringDocument

session = Session()

serverConfig = os.path.join(cheshire3Root, 'configs', 'serverConfig.xml')
serv = SimpleServer(session, serverConfig)

db = serv.get_object(session, 'db_c_dickens')
session.database = 'db_c_dickens'


# establish objects for later use
qf = db.get_object(session, 'defaultQueryFactory')
df = db.get_object(session, 'SimpleDocumentFactory')

concStore = db.get_object(session, 'concordanceStore')

authStore = db.get_object(session, 'authStore')

recStore = db.get_object(session, 'recordStore')
ampPreP = db.get_object(session, 'AmpPreParser')
xmlp = db.get_object(session, 'LxmlParser')


if ('-load' in sys.argv):
  indexWF = db.get_object(session, 'indexWorkflow')
  data = '/opt/clicdata/dickens_novels'
  df.load(session, data)
  recStore.begin_storing(session)
  db.begin_indexing(session)

  errorCount= 0
  for i, d in enumerate(df, start=1):
      doc = ampPreP.process_document(session, d)
      try:
          rec = xmlp.process_document(session, doc)
          genia = geniaTxr.process_record(session, rec)
          session.logger.log_info(session,
                                  'Record {0} created'.format(i)
                                  )
          rec2 = xmlp.process_document(session, genia)
          recStore.create_record(session, rec2)
          session.logger.log_info(session,
                                  'Record {0} stored'.format(i)
                                  )
          db.add_record(session, rec2)
          indexWF.process(session, rec2)
      except Exception as e:
          session.logger.log_error(session, str(e))
          errorCount += 1
          traceback.print_exc(file=sys.stdout)
  session.logger.log_info(session,
                          'Finished with {0} errors'.format(errorCount)
                          )
  recStore.commit_storing(session)
  db.commit_indexing(session)
