from elasticsearch import Elasticsearch

from elasticsearch.indexer import Indexer
from elasticsearch.searcher import Searcher

__author__ = 'alse'

elastic_search = Elasticsearch()
indexer = Indexer(elastic_search)
searcher = Searcher(elastic_search)