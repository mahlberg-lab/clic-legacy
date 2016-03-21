# -*- coding: utf-8 -*-

'''
Future module to handle the construction of cheshire3 CQL queries.
'''

class QueryBuilder(object):

    def __init__(self,
            search_term,
            corpus,
            index,
            namespace="c3"
            ):

        self.search_term = search_term
        self.corpus = corpus
        self.index = index
        # self.relation = and/any/exact/=/...
        # self.relation_modifier =
        self.namespace = namespace

    def define_corpus(self):
        subcorpus = []
        for itm in self.corpus:
            idx = 'book-idx'
            if itm in ['dickens', 'ntc']:
                idx = 'subcorpus-idx'
            subcorpus.append('{}.{} = "{}"'.format(self.namespace, idx, itm))
        return subcorpus

    def sanity_check(some_input):
        pass

    def to_CQL(self):
        corpus_li = self.define_corpus()
        corpus = " or ".join(corpus_li)
        # do we need quotes
        query_str = '({} and/cql.proxinfo c3.{} = "{}")'.format(
            corpus,
            self.index,
            self.search_term)
        return query_str

class CheshireQueryBuilder(QueryBuilder):
    pass
