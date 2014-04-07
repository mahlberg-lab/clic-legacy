from dickens.chapterDisplay import ChapterDisplay

idxName = 'chapter-idx'
terms = ['fog']

chapterdisplay = ChapterDisplay()

x = chapterdisplay.articleDisplay2(idxName, terms)
#x = chapterdisplay.getRS(idxName, terms)

print x