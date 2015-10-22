'''
Checks whether the pages of the CLiC site are up without having to use a browser.

Requirements:
 * pip install requests
 * pip install pytest

Run this file as follows:

    BASE_URL="http://test" py.test test.py
'''

import os
import requests
import unittest

BASE_URL = os.getenv('BASE_URL', 'http://birmingham.ac.uk/clic')


class TwoHundreds(unittest.TestCase):
    '''
    Checks whether the pages of the clic app actually give a 200 response
    (meaning the page was loaded without permission errors, servers errors or
    any other error).
    '''

    def setUp(self, base_url=''):
        self.base_url = BASE_URL

    def walk_through_urls(self, urls):
        for url in urls:
            compiled = self.base_url + url
            # only prints when the test fails
            print 'testing: ', compiled
            self.assertEqual(200, requests.get(compiled).status_code)

    def test_static_and_form_urls(self):
        urls = [ '/',
                 '/concordances',
                 '/keywords',
                 '/clusters',
                 '/subsets',
                 '/about',
                 '/documentation',
               ]
        self.walk_through_urls(urls)

    def test_get_requests(self):
        urls = ['/concordances/?testCollection=dickens&terms=fog&selectWords=whole&testIdxMod=chapter',
                '/keywords/?testIdxGroup=3gram-idx&testCollection=dickens&testIdxMod=quote&pValue=0.000001&refCollection=dickens&refIdxMod=non-quote',
                '/clusters/?testIdxGroup=5gram-idx&testCollection=dickens&testIdxMod=longsus',
                '/subsets/BH/long_suspensions/',
                '/chapter/BH/1/169/fog/#concordance',
                ]
        self.walk_through_urls(urls)
