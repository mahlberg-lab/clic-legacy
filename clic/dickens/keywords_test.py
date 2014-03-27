from clic.dickens.keywords import Keywords

import os
import re
from math import log1p

from cheshire3.document import StringDocument
from cheshire3.internal import cheshire3Root
from cheshire3.server import SimpleServer
from cheshire3.baseObjects import Session

cheshirePath = os.path.join('HOME', '/home/cheshire')

keywords = Keywords()

testIdxName = 'quote-3gram-idx'
testMaterials = ['dickens']
refIdxName = 'non-quote-3gram-idx'
refMaterials = ['dickens']

test = keywords.list_keywords(testIdxName, testMaterials, refIdxName, refMaterials)

print test