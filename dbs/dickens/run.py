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

from settings.settings import DATA_DIRECTORY

try:
    assert DATA_DIRECTORY
except:
    raise ImportError("You have not specified the project-wide settings.\
		       Please do so in settings.py.")
    

print DATA_DIRECTORY

# Launch a Cheshire session
session = Session()
serverConfig = os.path.join(cheshire3Root, 'configs', 'serverConfig.xml')
serv = SimpleServer(session, serverConfig)
db = serv.get_object(session, 'db_dickens')
session.database = 'db_dickens'
qf = db.get_object(session, 'defaultQueryFactory')
df = db.get_object(session, 'SimpleDocumentFactory')
concStore = db.get_object(session, 'concordanceStore')
# authStore = db.get_object(session, 'authStore')
recStore = db.get_object(session, 'recordStore')
ampPreP = db.get_object(session, 'AmpPreParser')
xmlp = db.get_object(session, 'LxmlParser')


### index 19C material
if ('--ntc' in sys.argv):
    geniaTxr = db.get_object(session, 'corpusTransformer')
    indexWF = db.get_object(session, 'indexWorkflow')
    data = DATA_DIRECTORY + 'ntc_novels'
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

## index Dickens material
if ('--dickens' in sys.argv):
    geniaTxr = db.get_object(session, 'corpusTransformer')
    indexWF = db.get_object(session, 'indexWorkflow')
    data = DATA_DIRECTORY + 'dickens_novels'
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


if ('--addIndex' in sys.argv):
    idx = db.get_object(session, 'idx-text-kwd-prox-unnrml')
    recStore = db.get_object(session, 'recordStore')
    idx.begin_indexing(session)
    session.logger.log_debug(session, recStore.id)
    session.logger.log_debug(session, idx.id)
#    recStore = [recStore.fetch_record(session, '96')]
    for i, rec in enumerate(recStore, start=1):
        session.logger.log_info(session, str(i))
        try:
            idx.index_record(session, rec)
        except Exception as e:
            session.logger.log_error(session, str(e))
            traceback.print_exc(file=sys.stdout)
    idx.commit_indexing(session)


if ('-loadAll' in sys.argv):
    geniaTxr = db.get_object(session, 'corpusTransformer')
    indexWF = db.get_object(session, 'indexWorkflow')
    data = DATA_DIRECTORY
    df.load(session, data)
    recStore.begin_storing(session)
    db.begin_indexing(session) 

    for d in df:
        doc = ampPreP.process_document(session, d)
        try:
            rec = xmlp.process_document(session, doc)
            print rec
            genia = geniaTxr.process_record(session, rec)
            rec2 = xmlp.process_document(session, genia)
            recStore.create_record(session, rec2)
            db.add_record(session, rec2)
            indexWF.process(session, rec2)
        except Exception as e:
            session.logger.log_error(session, str(e))
            traceback.print_exc(file=sys.stdout)

    recStore.commit_storing(session)
    db.commit_indexing(session)


if ('-indexAll' in sys.argv):
    indexWF = db.get_object(session, 'indexWorkflow')
    db.begin_indexing(session)
    for i, rec in enumerate(recStore, start=1):
        session.logger.log_info(session, str(i))
        try:
            indexWF.process(session, rec)
        except Exception as e:
            session.logger.log_error(session, str(e))
    db.commit_indexing(session)


if ('-index' in sys.argv):
    indexWF = db.get_object(session, 'indexWorkflow')
    db.begin_indexing(session)
    for i in range(0, 100):
        rec = recStore.fetch_record(session, '%d' % i)
        try:
            indexWF.process(session, rec)
        except Exception as e:
            session.logger.log_error(session, str(e))

    db.commit_indexing(session)


if ('-stru' in sys.argv):
    geniaTxr = db.get_object(session, 'corpusTransformer')
    recStore = db.get_object(session, 'struStore')
    df = db.get_object(session, 'StruDocumentFactory')
    df.load(session)
    idx = db.get_object(session, 'stru-idx')
    recStore.begin_storing(session)
    idx.begin_indexing(session)

    for d in df:
        doc = ampPreP.process_document(session, d)
        try:
            rec = xmlp.process_document(session, doc)
            session.logger.log_debug(session, rec)
            genia = geniaTxr.process_record(session, rec)
            rec2 = xmlp.process_document(session, genia)
            recStore.create_record(session, rec2)
            db.add_record(session, rec2)
            idx.index_record(session, rec2)
        except Exception as e:
            session.logger.log_error(session, str(e))
            traceback.print_exc(file=sys.stdout)
    recStore.commit_storing(session)
    idx.commit_indexing(session)


if ('-cont' in sys.argv):
    geniaTxr = db.get_object(session, 'corpusTransformer')
    recStore = db.get_object(session, 'contStore')
    df = db.get_object(session, 'ContDocumentFactory')
    df.load(session)
    idx = db.get_object(session, 'cont-idx')
    recStore.begin_storing(session)
    idx.begin_indexing(session)

    for d in df:
        doc = ampPreP.process_document(session, d)
        try:
            rec = xmlp.process_document(session, doc)
            session.logger.log_debug(session, rec)
            genia = geniaTxr.process_record(session, rec)
            rec2 = xmlp.process_document(session, genia)
            recStore.create_record(session, rec2)
            db.add_record(session, rec2)
            idx.index_record(session, rec2)
        except Exception as e:
            session.logger.log_error(session, str(e))
            traceback.print_exc(file=sys.stdout)
    recStore.commit_storing(session)
    idx.commit_indexing(session)


if ('-adduser' in sys.argv):
    un = raw_input('Please enter a username: ')
    if not un:
        inputError('You must enter a username for this user.')
    pw = getpass.getpass('Please enter a password for this user: ')
    if not (pw and len(pw)):
        inputError('You must enter a password for this user.')
    pw2 = getpass.getpass('Please re-enter the password to confirm: ')
    if pw != pw2:
        inputError('The two passwords submitted did not match. Please try again.')
    rn = raw_input('Real name of this user (not mandatory): ')
    addy = raw_input('Email address for this user (not mandatory): ')
    xml = read_file('xsl/admin.xml').replace('%USERNAME%', un)
    adminDict = {'%password%': crypt(pw, pw[:2]),
                 '%realName%': rn,
                 '%email%': addy
                 }
    for k,v in adminDict.iteritems():
        if v and len(v):
            xml = xml.replace(k, '\n  <%s>%s</%s>' % (k[1:-1],v,k[1:-1]))
        else:
            xml = xml.replace(k, '')
    doc = StringDocument(xml)
    rec = xmlp.process_document(session, doc)
    id = rec.process_xpath(session, '/config/@id')[0]
    rec.id = id
    authStore.store_record(session, rec)
    authStore.commit_storing(session)
    try:
        user = authStore.fetch_object(session, id)
    except c3errors.FileDoesNotExistException:
        print 'ERROR: User not successfully created. Please try again.'
    else:
        print 'OK: Username and passwords set for this user'
    #print user
    sys.exit() 
