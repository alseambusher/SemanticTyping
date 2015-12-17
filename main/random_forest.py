import os
import random

from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import RandomForest
from pyspark.mllib.util import MLUtils
from sklearn.datasets import dump_svmlight_file
from sklearn.feature_extraction import DictVectorizer

from lib import searcher
from main import train_model_dir, sc


class MyRandomForest:
    def __init__(self):
        self.file_path = 'rf_train_data.txt'
        self.model = None

    def generate_train_data(self, train_size):
        train_data = []
        for idx in range(train_size):
            size = random.randint(1, len(self.source_map) - 1)
            source_name = self.source_map.keys()[random.randint(0, len(self.source_map) - 1)]
            source = self.source_map[source_name]
            index_config = {'name': source.index_name, 'size': size}
            if searcher.is_index_exist(index_config):
                examples_map = searcher.search_all_types_data(index_config)
                for column_name in source.column_map.keys():
                    column = source.column_map[column_name]
                    feature_vectors = column.generate_candidate_types(examples_map, is_training=True)
                    train_data += feature_vectors.items()
            else:
                continue
        return train_data

    def train(self):
        train_data = sc.parallelize(self.generate_train_data(1000))
        self.model = RandomForest.trainClassifier(train_data, numClasses=2, numTrees=100, featureSubsetStrategy='auto',
                                                  impurity='gini', maxDepth=5, maxBins=32)

    def predict(self, test_data):
        return self.model.predict(sc.parallelize(test_data))
