from dickens.keywords import Keywords

keywords = Keywords()


testIdxName = 'quote-3gram-idx'
testMaterials = ['GE']
refIdxName = 'quote-3gram-idx'
refMaterials = ['BH']

test = keywords.list_keywords(testIdxName, testMaterials, refIdxName, refMaterials)

print test