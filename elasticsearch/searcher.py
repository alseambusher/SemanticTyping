from collections import defaultdict

from lib.utils import Utils
from main import sc

__author__ = "minh"


class Searcher:
    def __init__(self, es):
        self.es = es

    def search_all_types(self, index_config):
        result = self.es.search(index=Utils.get_index_name(index_config), doctype='semantic',
                                body={"query": {"match_all": {}}})

        return sc.parallelize(result['hits']['hits']).map(lambda hit: hit['semantic_type']).collect()

    def search_types_data(self, index_config, semantic_types):
        result = self.es.search(index=Utils.get_index_name(index_config), doc_type=','.join(semantic_types),
                                body={"query": {"match_all": {}}})

        return sc.parallelize(result['hits']['hits']).map(
            lambda hit: (hit['_type'], hit['_source'].items())).groupByKey().flatMap(lambda x: sc.parallelize(x[1]).map(
            lambda y: ((x[0], y[0]), y[1]) if isinstance(y[1], list) else ((x[0], y[0]), [y[1]]))).reduceByKey(
            lambda x, y: x + y).map(lambda x: (x[0][0], {x[0][1]: x[1]})).collectAsMap()

        return result

    def search_all_types_data(self, index_config):
        semantic_types = self.search_all_types(index_config)
        return self.search_types_data(index_config, semantic_types)

    def is_index_exist(self, index_config):
        return self.es.exists(index=Utils.get_index_name(index_config))
