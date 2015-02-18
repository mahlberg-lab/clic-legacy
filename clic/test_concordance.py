import unittest
from concordance_new import Concordancer_New


class TestConcordancerNewChapterIndex(unittest.TestCase):
    
    def test_create_concordance(self):
        """
        This is a very naive test to run whilst reviewing the create 
        concordance code. It's goal is simply to evaluate whether that
        function is still up an running.

        For that purpose it uses a hard-coded example
        """
        concordance = Concordancer_New()
        fog = concordance.create_concordance(terms="fog", 
					     idxName="chapter-idx", 
					     Materials=["dickens"], 
					     selectWords="whole")

	assert len(fog) == 95 	# 94 hits + one variable total_count in the list


class TestConcordancerNewQuoteIndex(unittest.TestCase):

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

	assert len(maybe) == 46 # 45 hits + one variable total_count in the list


if __name__ == '__main__':
    unittest.main()
