import unittest
import pandas as pd

from clic.keywords import log_likelihood, extract_keywords


class LogLikelihoodBasicTest(unittest.TestCase):
    '''
    Reference values calculated using http://ucrel.lancs.ac.uk/llwizard.html
    '''
    
    def setUp(self):
        self.data = pd.DataFrame([('hand', 540, 116000, 7525, 5451382), 
                                      ('hands', 227, 116000, 3635, 5451382),
                                      ('forehead', 29, 116000, 504, 5451382),
                                      ('head', 431, 116000, 5892, 5451382),
                                      ('neck', 16, 116000, 650, 5451382),
                                      ], 
                                      columns=('Type', 
                                               'Count_analysis', 
                                               'Total_analysis', 
                                               'Count_ref', 
                                               'Total_ref'))
        self.LLR = log_likelihood(self.data)
    
    def test_hand(self):
        hand = round(self.LLR.loc[self.LLR.Type == 'hand', 'LL'], 2)
        self.assertEqual(hand, 534.64)

    def test_hands(self):
        hands = round(self.LLR.loc[self.LLR.Type == 'hands', 'LL'], 2)
        self.assertEqual(hands, 183.53)    

    def test_forehead(self):
        forehead = round(self.LLR.loc[self.LLR.Type == 'forehead', 'LL'], 2)
        self.assertEqual(forehead, 20.50) 
        
    def test_head(self):
        head = round(self.LLR.loc[self.LLR.Type == 'head', 'LL'], 2)
        self.assertEqual(head, 437.88)         

    def test_neck(self):
        neck = round(self.LLR.loc[self.LLR.Type == 'neck', 'LL'], 2)
        self.assertEqual(neck, 0.32) 
        

class LogLikelihoodZeroes(unittest.TestCase):
    '''
    Reference values calculated using http://ucrel.lancs.ac.uk/llwizard.html
    '''
    
    def setUp(self):
        self.data = pd.DataFrame([('zero', 540, 116000, 0, 5451382), 
                                  ('zero_two', 7, 10000, 0, 100000), 
                                  ('zero_three', 0, 10000, 536, 100000), 
                                  ], 
                                  columns=('Type', 
                                           'Count_analysis', 
                                           'Total_analysis', 
                                           'Count_ref', 
                                           'Total_ref'))
        self.LLR = log_likelihood(self.data)
    
    def test_zero(self):
        zero = round(self.LLR.loc[self.LLR.Type == 'zero', 'LL'], 2)
        self.assertEqual(zero, 4180.78)

    def test_zero_two(self):
        zero_two = round(self.LLR.loc[self.LLR.Type == 'zero_two', 'LL'], 2)
        self.assertEqual(zero_two, 33.57)        

    def test_zero_three(self):
        '''
        The case where the count or expected count in the corpus of analysis is zero
        is not handled by the keywords module. NaN != 102.16
        '''
        zero_three = round(self.LLR.loc[self.LLR.Type == 'zero_three', 'LL'], 2)
        self.assertNotEqual(zero_three, 102.16)           
        
        
class LogLikelihoodSameValues(unittest.TestCase):
    '''
    Reference values calculated using http://ucrel.lancs.ac.uk/llwizard.html
    '''
    
    def setUp(self):
        self.data = pd.DataFrame([('zero', 10, 150, 10, 150), 
                                  ], 
                                  columns=('Type', 
                                           'Count_analysis', 
                                           'Total_analysis', 
                                           'Count_ref', 
                                           'Total_ref'))
        self.LLR = log_likelihood(self.data)
    
    def test_same_values(self):
        same_values = round(self.LLR.loc[self.LLR.Type == 'zero', 'LL'], 2)
        self.assertEqual(same_values, 0)
        
        
class KeywordExtraction(unittest.TestCase):
    '''
    Tests the filtering of the keyword results. Does not test the algorithm.
    '''
    
    def test_word_list_merging(self):
        pass
    
    def test_limit_rows(self):
        pass
        
    def test_p_value(self):
        pass
        
    def test_(self):
        pass
    
    
    
    