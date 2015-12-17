from collections import defaultdict

from lib.utils import Utils

__author__ = "minh"


class Searcher:
    def __init__(self, es):
        self.es = es

    def search_all_semantic_types(self, index_config):
        result = self.es.search(index=Utils.get_index_name(index_config), doctype='semantic',
                                body={"query": {"match_all": {}}})

        semantic_types = []

        for hit in result['hits']['hits']:
            semantic_types.append(hit['semantic_type'])

        return semantic_types

    def search_type_data(self, index_config, semantic_type):
        result = self.es.search(index=Utils.get_index_name(index_config), body={"query": {"match_all": {}}})

        examples_map = defaultdict(lambda: defaultdict(lambda: []))
        for hit in result['hits']['hits']:
            examples_map[hit['_type']]['numeric'] += hit['_source']['numeric']
            examples_map[hit['_type']]['historgram'] += hit['_source']['histogram']
