import unittest
from functools import partial

from clic.dickens.concordance_new import Concordancer_New

"""
Currently, the results from the concordance view look like this
(showing only one line in the concordance):

[94,                     # the total count
 [[' points ',           # the left text
   ' tenaciously ',
   ' to ',
   ' the ',
   ' pavement,',
   ' and ',
   ' accumulating ',
   ' at ',
   ' compound ',
   ' interest.'],
  ['Fog '],             # the search term or phrase
  [' everywhere.',      # the right text
   'Fog ',
   ' up ',
   ' the ',
   ' river,',
   ' where ',
   ' it ',
   ' flows ',
   ' among ',
   ' green '],
  ['BH', u'Bleak House', '1', '2', '9', '169', '2615'],   # book abbr, title, chapter, paragraph, sentence,  word, ???
  ['2', '9', '169', '354362']],                           # paragraph, sentence, word, ???
...

Because the list of results also contains an element that 
is not a hit (the first element, namely the total count).
We need to manually correct each result list
with this element this should be fixed by using a dictionary.
"""
correction = 1


class PhraseSearchOneTerm(unittest.TestCase):

    def setUp(self):
        concordance = Concordancer_New()
        self.create_concordance = partial(concordance.create_concordance, 
                                             terms="fog", 
                                             idxName="chapter-idx", 
                                             Materials=["dickens"], 
                                             selectWords="whole")

    def test_basic_query(self):
        # WordSmith (WS) has 96 because it includes compound nouns
        fog = self.create_concordance()
        self.assertEqual(len(fog) - correction, 94)  
        #TODO test whether the lines match with what one would expect

    def test_specific_book(self):
        # WS has 33 (because it includes fog-bank)
        fog = self.create_concordance(Materials=["BH"])
        self.assertEqual(len(fog) - correction, 32)
    
    def test_specific_corpus(self):
        fog = self.create_concordance(Materials=["ntc"])
        self.assertEqual(len(fog) - correction, 88)

    def test_quotes(self):
        fog = self.create_concordance(idxName="quote-idx")
        self.assertEqual(len(fog) - correction, 11)
        #TODO test whether the results in quotes are really in quotes

    def test_quotes_specific_book(self):
        fog = self.create_concordance(idxName="quote-idx",
                                            Materials=["ED"])
        self.assertEqual(len(fog) - correction, 3)

    def test_non_quotes(self):
        fog = self.create_concordance(idxName="non-quote-idx")
        self.assertEqual(len(fog) - correction, 42)

    def test_short_sus(self):
        fog = self.create_concordance(idxName="shortsus-idx")
        self.assertEqual(len(fog) - correction, 0)

    def test_long_sus(self):
        fog = self.create_concordance(idxName="longsus-idx")
        self.assertEqual(len(fog) - correction, 1)

    def test_long_sus(self):
        fog = self.create_concordance(idxName="longsus-idx", 
                                      Materials="BH")
        self.assertEqual(len(fog) - correction, 0)


class PhraseSearchOneTermQuotes(unittest.TestCase):
    pass


class PhraseSearchOneTermNonQuotes(unittest.TestCase):
    pass
    
    
class PhraseSearchOneTermShortSus(unittest.TestCase):
    pass


class PhraseSearchOneTermLongSus(unittest.TestCase):
    pass


class OrSearchMultipleTerms(unittest.TestCase):
    
    def setUp(self):
        self.concordance = Concordancer_New()
    
    
    def test_create_concordance(self):
        fog = self.concordance.create_concordance(terms="dense fog", 
                                             idxName="chapter-idx", 
                                             Materials=["dickens"], 
                                             selectWords="any")

        # the only the thing that changes is the order of the terms
        # which should not affect the results
        dense = self.concordance.create_concordance(terms="fog dense", 
                                             idxName="chapter-idx", 
                                             Materials=["dickens"], 
                                             selectWords="any")
        
        self.assertEqual(fog, dense)


class PhraseSearchMultipleTerms(unittest.TestCase):

    def test_create_concordance(self):
        concordance = Concordancer_New()
        fog = concordance.create_concordance(terms="dense fog", 
                                             idxName="chapter-idx", 
                                             Materials=["dickens"], 
                                             selectWords="whole")

        assert len(fog) - correction == 3 


class PhraseSearchOneTermQuoteIndex(unittest.TestCase):

    def test_create_concordance(self):
        """
        This is another naive test focusing on searching in quotes 

        It also uses a hard-coded example
        """
        concordance = Concordancer_New()
        maybe = concordance.create_concordance(terms="maybe", 
                                             idxName="quote-idx", 
                                             Materials=["dickens"], 
                                             selectWords="whole")

        assert len(maybe) - correction == 45 # 45 hits + one variable total_count in the list


class OrSearchOneTerm:
    pass

if __name__ == '__main__':
    unittest.main()
