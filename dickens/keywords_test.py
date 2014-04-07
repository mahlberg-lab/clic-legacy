from dickens.keywords import Keywords

keywords = Keywords()


testIdxName = 'quote-4gram-idx'
#testMaterials = ['dickens']
testMaterials = ['GE']
refIdxName = 'non-quote-4gram-idx'
#refMaterials = ['dickens']
refMaterials = ['GE']

test = keywords.list_keywords(testIdxName, testMaterials, refIdxName, refMaterials)

print test

filewrite = open('/home/aezros/keywords_GE_quotes.txt', 'w')
filewrite.write(''.join('{"keywords" : ' + '%s' + '}') % str(test))