import os
import re

from cheshire3.document import StringDocument
from cheshire3.internal import cheshire3Root
from cheshire3.server import SimpleServer
from cheshire3.baseObjects import Session

from dickens.concordance_new import Concordancer_New

terms = 'be with you'
#terms = 'youthful'
idxName = 'quote'
#idxName = 'sentence'
#idxName = 'chapter'
Materials = ['BH']
wordWindow = 20

concordance = Concordancer_New()

conc = concordance.create_concordance(terms, idxName, wordWindow)#, Materials)

print conc
