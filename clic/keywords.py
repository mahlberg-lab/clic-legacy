# -*- coding: utf-8 -*-

'''
Module to compute keywords (words that are used significantly more frequently
in one corpus than they are in a reference corpus). 

The statistical measure used is
Log Likelihood as explained by Rayson and Garside 
(http://ucrel.lancs.ac.uk/people/paul/publications/rg_acl2000.pdf)

Usage as follows:
-----------------

    analysis = pd.DataFrame([('a', 2500), ('the', 25000)], columns=('Type', 'Count'))
    reference = pd.DataFrame([('a', 10), ('the', 10)], columns=('Type', 'Count'))

    result = extract_keywords(analysis, 
                     reference, 
                     tokencount_analysis=20, 
                     tokencount_reference=100, 
                     round_values=True, 
                     limit_rows=3)
    result
    
    keywords_to_json(result)

Or using text files as input:
-----------------------------

    from collections import Counter

    with open('~/data/input/DNov/BH.txt') as inputfile:
        bh = inputfile.read().split()
        bh = Counter(bh)

    with open('~/data/input/DNov/OT.txt') as inputfile:
        ot = inputfile.read().split()
        ot = Counter(ot)
        
    bh_df  = pd.DataFrame(bh.items(), columns=['Type', 'Count'])
    ot_df  = pd.DataFrame(ot.items(), columns=['Type', 'Count'])

    extract_keywords(bh_df, 
                     ot_df, 
                     tokencount_analysis=bh_df.Count.sum(), 
                     tokencount_reference=ot_df.Count.sum(), 
                     round_values=True,)

'''

import os
import operator
import pandas as pd
import numpy as np

from cheshire3.document import StringDocument
from cheshire3.internal import cheshire3Root
from cheshire3.server import SimpleServer
from cheshire3.baseObjects import Session


def format_wordlist(types, counts, total=None):
    '''
    Helper function to convert lists with information into a dataframe.
    '''
    pass
    
def log_likelihood(counts):
    '''
    This function uses vector calculations to compute LL values. 
    
    Input: dataframe that is formatted as follows:
    
        Type, 
        Count_analysis, 
        Total_analysis, 
        Count_ref, 
        Total_ref
    
    Output: dataframe that is formatted as follows:
    
         Type, 
         Count_analysis, 
         Total_analysis, 
         Count_ref, 
         Total_ref, 
         Expected_count_analysis,
         Expected_count_ref
         LL
         
    Hapax legomena in the Count_analysis are not deleted.
    It is expected that Count_analysis and Expected_count_analysis are not zero. 
    '''
    
    # compute expected values
    counts.loc[:,'Expected_count_analysis'] = counts['Total_analysis'] * (counts['Count_analysis'] + counts['Count_ref']) / (counts['Total_analysis'] + counts['Total_ref'])
    counts.loc[:,'Expected_count_ref'] = counts['Total_ref'] * (counts['Count_analysis'] + counts['Count_ref']) / (counts['Total_analysis'] + counts['Total_ref'])

    # define variables to avoid cluttering
    a = counts['Count_analysis']
    exp_a = counts['Expected_count_analysis']
    b = counts['Count_ref']
    exp_b = counts['Expected_count_ref']

    # log likelihood if count or expected count in the ref corpus are 0
    # the order of the LL computation is important
    # these cases do NOT handle wordlists where the type does not occur in the corpus of analysis
    counts.loc[(b == 0) | (exp_b == 0), 'LL'] = 2*(a * np.log(a/exp_a)) 

    # compute log likelihood for normal cases
    # do not use the following as it will overwrite the specific cases above: 
    # counts.loc[:,'LL'] = 2*((a * np.log(a/exp_a)) + (b * np.log(b/exp_b)))
    counts.loc[(b != 0) & (exp_b != 0), 'LL'] = 2*((a * np.log(a/exp_a)) + (b * np.log(b/exp_b)))
    
    # sort the results
    keywords = counts.sort_values('LL', ascending=False)
    
    return keywords
    
def extract_keywords(wordlist_analysis, 
             wordlist_reference,
             tokencount_analysis,
             tokencount_reference,
             p_value=0.0001,
             exclude_underused=True,
             freq_cut_off=5,
             round_values=True,
             limit_rows=False
            ):   
    '''
    This is the core method for keyword extraction. It provides a number 
    of handles to select sections of the data and/or adapt the input for the
    formula. 
    
    Input = Two dataframes with columns 'Type', and 'Count' and 
            two total tokencounts
    
    Output = An aligned dataframe which is sorted on the LL value and maybe filter 
             using the following handles:
             
        - p_value: limits the keywords based on their converted p_value. A p_value of 0.0001
                   will select keywords that have 0.0001 *or less* as their p_value. It is a 
                   cut-off. One can choose one out of four values: 0.0001, 0.001, 0.01, or 0.05.
                   If any other value is chosen, it is ignored and no filtering on p_value is done.
        
        - exclude_underused: if True (default) it filters the result by excluding tokens that are 
                             statistically underused.
                             
        - freq_cut_off: limits the wordlist_analysis to words that have the freq_cut_off (inclusive) 
                        as minimal frequency. 5 is a sane default for Log Likelihood. If one does not 
                        want frequency-based filtering, set a value of 0.
                        
        - round_values: if True (default) it rounds the columns with expected frequencies and LL 
                        to 2 decimals.
        
        - limit_rows: if a number (for instance, 100), it limits the result to the number of rows 
                      specified. If false, rows are not limited. 
    
    The defaults are reasonably sane: 
     - a token needs to occur at least 5 times in the corpus of analysis
     - a high p-value is set
     - no filtering of the rows takes place
     - the underused tokens are excluded
     - rounding is active

    For more information on the algorithm, cf. log_likelihood().
    
    The first column contains the indeces for the original merged dataframe. It does not display
    a rank and it should be ignored for keyword analysis (to be more precise: it displays the 
    frequency rank of the token in the corpus of analysis).
    '''

    # select only the Type and Count columns
    wordlist_analysis = wordlist_analysis[['Type', 'Count']]
    wordlist_reference = wordlist_reference[['Type', 'Count']]
    
    # limit with a simple frequency cut-off, does not filter the corpus of reference
    wordlist_analysis = wordlist_analysis.loc[wordlist_analysis.Count >= freq_cut_off]

    # merge and align the two wordlists
    merged = wordlist_analysis.merge(wordlist_reference, on='Type', how='left', suffixes=('_analysis', '_ref')).fillna(0)
    # float64 to int64 because pandas int64 does not handle NaN
    merged.loc[:,'Count_ref'] = merged['Count_ref'].astype(int)
    
    # prepare object for computation
    if not tokencount_analysis:
        raise IOError, 'You did not provide a total token count for the corpus of analysis'
    merged.loc[:,'Total_analysis'] = tokencount_analysis
    
    if not tokencount_reference:
        raise IOError, 'You did not provide a total token count for the corpus of reference'
    merged.loc[:,'Total_ref'] = tokencount_reference
    keywords = merged.loc[:,['Type', 'Count_analysis', 'Total_analysis', 'Count_ref', 'Total_ref']]

    # compute keyness
    keywords = log_likelihood(keywords)
    
    # over and underused
    keywords.loc[:,'Use'] = '0'
    keywords.loc[keywords.Count_analysis > keywords.Expected_count_analysis, 'Use'] = '+'
    keywords.loc[keywords.Count_analysis < keywords.Expected_count_analysis, 'Use'] = '-'

    if exclude_underused:
        keywords = keywords.loc[keywords['Use'] == '+',:]
    
    # translate LL value to p-value
    keywords.loc[:,'p'] = 'p >= 0.05'
    keywords.loc[keywords['LL'] >= 3.84,'p'] = 'p < 0.05'
    keywords.loc[keywords['LL'] >= 6.63,'p'] = 'p < 0.01'
    keywords.loc[keywords['LL'] >= 10.83,'p'] = 'p < 0.001'
    keywords.loc[keywords['LL'] >= 15.13,'p'] = 'p < 0.0001'        
    
    # limit the keywords to the p-value
    # if the p cut-off does not match either of the conditions, no filtering is done
    if p_value == 0.0001:
        keywords = keywords[keywords['LL'] >= 15.13]
    if p_value == 0.001:
        keywords = keywords[keywords['LL'] >= 10.83]
    if p_value == 0.01:
        keywords = keywords[keywords['LL'] >= 6.63]
    if p_value == 0.05:
        keywords = keywords[keywords['LL'] >= 3.84]
        
    if round_values:
        keywords = keywords.round({'LL':2, 'Expected_count_analysis':2, 'Expected_count_ref':2})
    
    if limit_rows:
        return keywords.iloc[:limit_rows]
    
    return keywords
    
def keywords_to_json(keywords):
    '''
    Transforms a keywords table into a json array. 
    It is specifically tailored at the CLiC Dickens interface.
    '''
    keywords.loc[:,'Empty'] = ''
    keywords = keywords[['Empty',
                        'Type', 
                        'Count_analysis', 
                        'Expected_count_analysis', 
                        'Count_ref', 
                        'Expected_count_ref',
                        'LL',
                        'p',
                        'Use']]
    return keywords.to_json(orient='values') 
