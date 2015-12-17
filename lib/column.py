import re

from lib.utils import Utils
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

    def add_value(self, value):
        self.value_list.append(value)
        self.content_length += value.split()

        if Utils.is_number(value):
            self.numeric_count += 1

    def is_numeric(self):
        return self.numeric_count * 1.0 / len(self.value_list) >= 0.7

    def predict_type(self, train_examples_map, rf):
        feature_vectors, class_labels = self.generate_candidate_types()
        semantic_types = []
        for semantic_type in feature_vectors.keys():
            prob = rf.predict_proba([feature_vectors[semantic_type]])
            if prob > 0.5:
                semantic_types.append(prob, semantic_type)
        return sorted(semantic_types)

    def generate_candidate_types(self, train_examples_map, vectorizer):
        integrated_test = IntegratedTest(self, train_examples_map)
        feature_vectors, class_labels = integrated_test.get_all_feature_vectors()
        for key in feature_vectors.keys():
            feature_vectors[key] = vectorizer.transform([feature_vectors[key]])[0]
        return feature_vectors, class_labels
