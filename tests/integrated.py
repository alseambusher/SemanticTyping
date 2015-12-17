from collections import OrderedDict

from pyspark.mllib.regression import LabeledPoint

from lib.utils import Utils
from tests.label import content_length_test, label_text_test
from tests.textual import *
import re
from numeric import *

__author__ = 'alse'


class IntegratedTest:
    IS_NUMERIC = "IS_NUM"
    KS_TEST = "KS"
    MW_NUM_TEST = "MW_NUM"
    MW_TEST = "MW"
    ANOVA_TEST = "ANOVA"
    SOFT_TFIDF_TEST = "Soft TFIDF"
    ABBR_TEST = "ABBR"
    LBL_ABBR_TEST = "LBL ABBR"
    LBL_TEST = "LBL"
    VALUE_SIZE = "SIZE"

    feature_names = [IS_NUMERIC, KS_TEST, MW_NUM_TEST, MW_TEST, ANOVA_TEST, SOFT_TFIDF_TEST, ABBR_TEST]

    def __init__(self, column, train_examples_map, sc):
        self.train_examples_map = train_examples_map
        self.test_examples = column.value_list
        self.true_label = column.semantic_type
        self.name = column.name
        self.numeric_test_examples = Utils.clean_examples_numeric(self.test_examples)
        self.is_numeric = column.is_numeric()

        self.sc = sc

    def get_all_feature_vectors(self):
        feature_vectors = {}

        """
            TODO for tfidf score map
            List<SemanticTypeLabel> tfidfResults = new Searcher(new IntegratedTypingHandler("semantic-labeling").getIndexDirectory(2),
            Indexer.CONTENT_FIELD_NAME).getTopK(15, sb.toString());
        """
        for label in self.train_examples_map.keys():
            result_map = OrderedDict()
            self.test_histogram(label, result_map)
            self.test_numeric(label, result_map)
            self.test_textual(label, result_map)
            self.test_label(label, result_map)

            if label == self.true_label:
                class_label = 1
            else:
                class_label = 0

            labeled_point = LabeledPoint(class_label, result_map.items())

            feature_vectors[label] = labeled_point

        return feature_vectors

    def test_histogram(self, label, result_map):
        hist_examples = Utils.get_distribution(self.test_examples)
        result_map[self.ANOVA_TEST] = anova_test(self.train_examples_map[label]['histogram'], hist_examples,
                                                 self.sc)
        result_map[self.MW_TEST] = mann_whitney_num_test(self.train_examples_map[label]['histogram'], hist_examples,
                                                         self.sc)

    def test_numeric(self, label, result_map):
        if not self.is_numeric or not self.train_examples_map[label]['numeric']:
            result_map[self.KS_TEST] = 0.0
            result_map[self.MW_NUM_TEST] = 0.0
        else:
            result_map[self.KS_TEST] = kolmogorov_smirnov_test(self.train_examples_map[label]['numeric'],
                                                               self.numeric_test_examples, self.sc)
            result_map[self.MW_NUM_TEST] = mann_whitney_num_test(self.train_examples_map[label]['numeric'],
                                                                 self.numeric_test_examples, self.sc)

    def test_label(self, label, result_map):
        result_map[self.LBL_ABBR_TEST] = abbr_test(self.train_examples_map[label]['meta'], self.name)
        result_map[self.LBL_TEST] = label_text_test(self.train_examples_map[label]['meta'], self.name)
        result_map[self.VALUE_SIZE] = content_length_test(self.train_examples_map[label]['meta'], self.name)

    def test_textual(self, label, result_map):
        if self.is_numeric:
            result_map[self.SOFT_TFIDF_TEST] = 0.0
            result_map[self.ABBR_TEST] = 0.0
        else:
            result_map[self.SOFT_TFIDF_TEST] = tfidf(self.train_examples_map[label]['textual'], self.test_examples)
            result_map[self.ABBR_TEST] = abbr_test(self.train_examples_map[label]['textual'], self.test_examples)


