from lib.utils import Utils

__author__ = "minh"


class Indexer:
    def __init__(self, es):
        self.es = es

    def index_column(self, column, index_config):
        doc_body = {
            'metadata': {
                'name': column.name,
                'semantic_type': column.semantic_type,
                'content_length': column.content_length,
                'data_size': len(column.value_list)
            },
            'values': column.value_list,
            'histogram': Utils.get_distribution(column.value_list)}
        if column.is_numeric():
            doc_body['numeric'] = Utils.clean_examples_numeric(column.value_list)
        else:
            doc_body['textual'] = " ".join(column.value_list)

        self.es.index(index=Utils.get_index_name(index_config), doc_type=column.semantic_type,
                      body=doc_body)

        doc_body = {
            'semantic_type': column.semantic_type
        }

        if not self.es.search_exists(index=Utils.get_index_name(index_config),
                                     doc_type='semantic', body=doc_body):
            self.es.index(index=Utils.get_index_name(index_config), doc_type='semantic', id=1,
                          body=doc_body)

    def index_source(self, source, index_config):
        for column in source.column_map.values():
            self.index_column(column, index_config)
