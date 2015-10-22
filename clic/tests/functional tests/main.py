'''
Checks whether the pages of the CLiC site are up without having to use a browser.

Requirements:
 * pip install requests
 * pip install pytest

Run this file as follows:

    BASE_URL="http://test" py.test test.py

New logic taken from: http://blog.kevinastone.com/generate-your-tests.html
This generates methods on the fly to avoid having to write too many functions.
'''

import os
import requests
import unittest

BASE_URL = os.getenv('BASE_URL', 'http://birmingham.ac.uk/clic')

#### META

def make_method(func, url):
    '''
    Takes a functions and an argument and makes it into a method that can be
    placed inside a TestCase
    '''

    def test_url(self):
        func(self, url)

    # changes the placeholder function name to something meaningful
    test_url.__name__ = 'test_{func}_{url}'.format(func=func.__name__, url=url)
    return test_url


def generate(func, *urls):
    """
    Take a TestCase and add a test method for each input
    """
    def decorator(klass):
        for url in urls:
            test_url = make_method(func, url)
            setattr(klass, test_url.__name__, test_url)
        return klass

    return decorator

### ACTUAL TESTING

urls = [ '/',
         '/concordances',
         '/keywords',
         '/clusters',
         '/subsets',
         '/about',
         '/documentation',
       ]

get_urls = ['/concordances/?testCollection=dickens&terms=fog&selectWords=whole&testIdxMod=chapter',
        '/keywords/?testIdxGroup=3gram-idx&testCollection=dickens&testIdxMod=quote&pValue=0.000001&refCollection=dickens&refIdxMod=non-quote',
        '/clusters/?testIdxGroup=5gram-idx&testCollection=dickens&testIdxMod=longsus',
        '/subsets/BH/long_suspensions/',
        '/chapter/BH/1/169/fog/#concordance',
        ]

def assert_response_code_is_200(self, url):
    compiled = self.base_url + url
    self.assertEqual(requests.get(compiled).status_code, 200)

@generate(assert_response_code_is_200, *urls)
@generate(assert_response_code_is_200, *get_urls)
class TwoHundreds(unittest.TestCase):
    '''
    Checks whether the pages of the clic app actually give a 200 response
    (meaning the page was loaded without permission errors, servers errors or
    any other error).
    '''

    def setUp(self, base_url=''):
        self.base_url = BASE_URL
