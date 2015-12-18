import os
import random
from itertools import cycle, repeat

import re
from elasticsearch import Elasticsearch
from pyspark.mllib.tree import RandomForest, RandomForestModel

from lib.source import Source

__author__ = 'alse'


class SemanticLabeler:
    def __init__(self, sc):
        self.sc = sc
        self.source_map = {}
        self.es = Elasticsearch()

    def read_data_sources(self, folder_path):
        data_folder_path = os.path.join(folder_path, "data")
        model_folder_path = os.path.join(folder_path, "model")

        for filename in os.listdir(data_folder_path):
            extension = os.path.splitext(filename)[1]

            source = Source(os.path.splitext(filename)[0], self.sc)
            file_path = os.path.join(data_folder_path, filename)

            if extension == ".csv":
                source.read_data_from_csv(file_path)
            elif extension == ".json":
                source.read_data_from_json(file_path)
            elif extension == ".xml":
                source.read_data_from_xml(file_path)
            self.source_map[filename] = source

        for filename in os.listdir(model_folder_path):
            source = self.source_map[os.path.splitext(os.path.splitext(filename)[0])[0]]

            source.read_semantic_type_json(os.path.join(model_folder_path, filename))

    # TODO
    def train_random_forest(self, train_size):
        for idx in range(train_size):
            size = random.randint(1, len(self.source_map) - 1)
            source_name = self.source_map.keys()[random.randint(0, len(self.source_map) - 1)]
            source = self.source_map[source_name]
            if self.es.exists(index="%s!%s" % (source.index_name, size)):
                examples_map = source.load(self.es, index_config={'size': size})

                for column_name in source.column_map.keys():
                    column = source.column_map[column_name]
                    column.predict_type(examples_map, is_training=True)
            else:
                continue

    # TODO
    def train_semantic_types(self, size_list):
        for idx in range(len(self.source_map)):
            for size in size_list:
                for source_name in (self.source_map.keys() * 2)[idx + 1: idx + size + 1]:
                    source = self.source_map[source_name]
                    source.save(es=self.es,
                                index_config={'size': size})

    # TODO
    def test_semantic_types(self):
        pass
