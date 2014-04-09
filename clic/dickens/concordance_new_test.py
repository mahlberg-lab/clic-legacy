import os
import re
import timeit
import json
import time

start = time.time()

from cheshire3.document import StringDocument
from cheshire3.internal import cheshire3Root
from cheshire3.server import SimpleServer
from cheshire3.baseObjects import Session

from clic.dickens.concordance_new import Concordancer_New

terms = 'hands'
#terms = 'youthful'
#idxName = 'non-quote-idx'
#idxName = 'sentence-idx'
idxName = 'chapter-idx'
Materials = ['dickens']
wordWindow = 10
selectWords = 'whole'

args = [terms, idxName, wordWindow, Materials, selectWords]

def getConcordance(args):   

    concordance = Concordancer_New()     
    conc = concordance.create_concordance(args[0], args[1], args[2], args[3], args[4])
    return {'concordances' : conc}

   

x = json.dumps(getConcordance(args))

print x
print "it took", time.time() - start, "seconds to execute the script"

# filewrite = open('/home/aezros/concordance_300hits', 'w')
# filewrite.write(x)


