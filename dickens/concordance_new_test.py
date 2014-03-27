import os
import re

from cheshire3.document import StringDocument
from cheshire3.internal import cheshire3Root
from cheshire3.server import SimpleServer
from cheshire3.baseObjects import Session

from clic.dickens.concordance_new import Concordancer

terms = 'be with you'
idxName = 'quote'
#idxName = 'sentence'
Materials = ['BH']

concordance = Concordancer()

conc = concordance.create_concordance(terms, idxName)#, Materials)
