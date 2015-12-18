from lib.utils import Utils
from tests.label import content_length_test, label_text_test
from tests.textual import *
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

    feature_names = [ANOVA_TEST, MW_TEST, KS_TEST, MW_NUM_TEST, LBL_ABBR_TEST, LBL_TEST, VALUE_SIZE, SOFT_TFIDF_TEST,
                     ABBR_TEST]

    def __init__(self, column, train_examples_map, sc):
        self.train_examples_map = train_examples_map
        self.test_examples = column.value_list
        self.true_label = column.semantic_type
        self.name = column.name
        self.numeric_test_examples = Utils.clean_examples_numeric(self.test_examples)
        self.is_numeric = column.is_numeric()
        self.hist_examples = Utils.get_distribution(self.test_examples)

        self.sc = sc

    def get_all_feature_vectors(self):
        feature_vectors = {}
        class_labels = {}
        labels = self.train_examples_map.keys()
        labelsRDD = self.sc.parallalize(labels)
        # TODO now all the tests for a given label run sequentially. Make them run in parallel
        tests = labelsRDD.flatMap(
            lambda x: self.test_histogram(x) + self.test_numeric(x) + self.test_label(x) + self.test_textual(x))
        results = tests.take(len(self.feature_names)*len(labels))
        for i in xrange(len(labels)):

            if labels[i] == self.true_label:
                class_labels[labels[i]] = True
            else:
                class_labels[labels[i]] = False

            feature_vectors[labels[i]] = results[i*len(self.feature_names): (i+1)*len(self.feature_names)]

        return feature_vectors, class_labels

    def test_histogram(self, label):
        hist_examples = self.hist_examples
        return anova_test(self.train_examples_map[label]['histogram'], hist_examples), mann_whitney_num_test(
            self.train_examples_map[label]['histogram'], hist_examples)

    def test_numeric(self, label):
        if not self.is_numeric or not self.train_examples_map[label]['numeric']:
            return 0.0, 0.0
        else:
            return kolmogorov_smirnov_test(self.train_examples_map[label]['numeric'],
                                           self.numeric_test_examples), mann_whitney_num_test(
                self.train_examples_map[label]['numeric'],
                self.numeric_test_examples)

    def test_label(self, label):
        return abbr_test(self.train_examples_map[label]['meta'], self.name), label_text_test(
            self.train_examples_map[label]['meta'], self.name), content_length_test(
            self.train_examples_map[label]['meta'], self.name)

    def test_textual(self, label):
        if self.is_numeric:
            return 0.0, 0.0
        else:
            return tfidf(self.train_examples_map[label]['textual'], self.test_examples), abbr_test(
                self.train_examples_map[label]['textual'], self.test_examples)
