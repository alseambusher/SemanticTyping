import re

from lib.utils import Utils
from main import sc
from tests.integrated import IntegratedTest

__author__ = 'alse'


class Column:
    def __init__(self, name, index_config):
        self.name = name
        self.value_list = []
        self.semantic_type = None
        self.content_length = 0
        self.numeric_count = 0
        self.index_config = index_config
        self.histogram_list = None
        self.numeric_list = None
        self.sample_list = None
        self.value_text = ""
        self.is_prepared = False

    def add_value(self, value):
        self.value_list.append(value)
        self.content_length += value.split()

        if Utils.is_number(value):
            self.numeric_count += 1

    def prepare_data(self):
        if not self.is_prepared:
            self.histogram_list = Utils.get_distribution(self.value_list)
            self.numeric_list = Utils.clean_examples_numeric(self.value_list)
            if self.is_numeric():
                self.sample_list = sc.parallelize(self.numeric_list).sample(False,
                                                                            100.0 / len(self.numeric_list)).collect()
            else:
                self.value_text = sc.parallelize(self.value_list).map(lambda x: " %s " % x).reduce(lambda x, y: x + y)
            self.is_prepared = True

    def is_numeric(self):
        return self.numeric_count * 1.0 / len(self.value_list) >= 0.7

    def predict_type(self, train_examples_map, rf):
        feature_vectors, class_labels = self.generate_candidate_types()
        semantic_types = []
        for semantic_type in feature_vectors.keys():
            prob = rf.predict_proba([feature_vectors[semantic_type]])
            if prob > 0.5:
                semantic_types.append((prob, semantic_type))
        return sorted(semantic_types)

    def generate_candidate_types(self, train_examples_map, vectorizer):
        integrated_test = IntegratedTest(self, train_examples_map)
        return integrated_test.get_all_feature_vectors()
