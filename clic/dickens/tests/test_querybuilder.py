from clic.querybuilder import QueryBuilder

from unittest import TestCase


class SimpleQuery(TestCase):

    def test_phrase(self):
        query = QueryBuilder(search_term="fog", corpus=["dickens"], index="quote-idx")
        # NOTE figure out if any is quicker
        expected_result = """(c3.subcorpus-idx = "dickens" and/cql.proxinfo c3.quote-idx = "fog")"""
        self.assertEqual(expected_result, query.to_CQL())
        #query = QueryBuilder(phrase_search = "'the dense fog'")
        #self.assertEqual('c3. ... ', query.to_CQL())
        #query = QueryBuilder(phrase_search = '"the dense fog"')
        #self.assertEqual('c3. ... ', query.to_CQL())

    def test_any(self):
        query = QueryBuilder(any_search = "fog dense")
        self.assertEqual('c3. ...', query.to_CQL())
        query = QueryBuilder(any_search = "fog OR dense")
        self.assertEqual('c3. ...', query.to_CQL())

    def test_and(self):
        query = QueryBuilder(and_search = "dense in fog")
        self.assertEqual('c3. ...', query.to_CQL())
        query = QueryBuilder(and_search = "dense AND in AND fog")
        self.assertEqual('c3. ...', query.to_CQL())

    def test_not(self):
        query = QueryBuilder(not_search = "dense NOT fog")
        self.assertEqual('c3. ...', query.to_CQL())

class ComplexQuery(TestCase):
    pass
