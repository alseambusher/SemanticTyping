from tests.label import content_length_test, label_text_test
from tests.textual import *

__author__ = 'alse'
import re
from numeric import *


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

    is_numeric = False
    test_examples = []
    textual_example_map = {}
    histogram_example_map = {}
    numeric_example_map = {}
    meta_example_map = {}
    result_map = {}
    true_label = None
    name = None
    tfidf_score_map = None
    numeric_regex = re.compile(
            "^((\\-)?[0-9]{1,3}(,[0-9]{3})+(\\.[0-9]+)?)|((\\-)?[0-9]*\\.[0-9]+)|((\\-)?[0-9]+)|((\\-)?[0-9]*\\.?[0-9]+"
            "([eE][-+]?[0-9]+)?)$")

    def __init__(self, true_label, column_name, test_examples, textual_example_map, histogram_example_map,
                 numeric_example_map,
                 meta_example_map, is_numeric, sc):
        self.test_examples = test_examples
        self.textual_example_map = textual_example_map
        self.histogram_example_map = histogram_example_map
        self.numeric_example_map = numeric_example_map
        self.meta_example_map = meta_example_map
        self.is_numeric = is_numeric
        self.true_label = true_label
        self.name = column_name
        self.numeric_test_examples = self.clean_examples_numeric(self.test_examples)
        self.sc = sc

    def get_all_feature_vectors(self):
        feature_vectors = []
        sb = " ".join(self.test_examples)
        self.tfidf_score_map = {}
        """
                TODO for tfidf score map
                List<SemanticTypeLabel> tfidfResults = new Searcher(new IntegratedTypingHandler("semantic-labeling").getIndexDirectory(2),
                Indexer.CONTENT_FIELD_NAME).getTopK(15, sb.toString());
        """
        for label in self.histogram_example_map:
            result_map = {}
            self.test_histogram(label, result_map)
            self.test_numeric(label, result_map)
            self.test_textual(label, result_map)
            self.test_label(label, result_map)

            feature_vectors.append(result_map)

        return feature_vectors

    def test_histogram(self, label, result_map):
        highest_examples = IntegratedTest.get_distribution(self.test_examples)
        result_map[self.KS_TEST] = kolmogorov_smirnov_test(self.numeric_example_map[label], highest_examples,
                                                           self.sc)
        result_map[self.KS_TEST] = mann_whitney_num_test(self.numeric_example_map[label], highest_examples,
                                                         self.sc)

    def test_numeric(self, label, result_map):
        if not self.is_numeric or label not in self.numeric_example_map:
            result_map[self.KS_TEST] = 0.0
            result_map[self.MW_NUM_TEST] = 0.0
        else:
            result_map[self.KS_TEST] = kolmogorov_smirnov_test(self.numeric_example_map[label],
                                                               self.numeric_test_examples, self.sc)
            result_map[self.KS_TEST] = mann_whitney_num_test(self.numeric_example_map[label],
                                                             self.numeric_test_examples, self.sc)

    def test_label(self, label, result_map):
        result_map[self.LBL_ABBR_TEST] = abbr_test(self.meta_example_map[label], self.name)
        result_map[self.LBL_TEST] = label_text_test(self.meta_example_map[label], self.name)
        result_map[self.VALUE_SIZE] = content_length_test(self.meta_example_map[label], self.name)

    def test_textual(self, label, result_map):
        if label not in self.numeric_example_map:
            result_map[self.SOFT_TFIDF_TEST] = 0.0
            result_map[self.ABBR_TEST] = 0.0
        else:
            result_map[self.SOFT_TFIDF_TEST] = tfidf(self.textual_example_map[label], self.test_examples)
            result_map[self.ABBR_TEST] = abbr_test(self.textual_example_map[label], self.test_examples)

    def clean_examples_numeric(self, examples):
        cleaned = []
        for example in examples:
            if self.numeric_regex.match(example.strip()):
                cleaned.append(float(example.strip()))
        return cleaned

    @staticmethod
    def get_distribution(data):
        distribution_map = {}
        for entry in data:
            if entry in distribution_map:
                distribution_map[entry] += 1
            else:
                distribution_map[entry] = 1.0

        sample_list = []
        for idx, distribution in enumerate(sorted(distribution_map.values())):
            sample_list.extend([idx] * int(distribution / len(data) * 100))
            # TODO add pseudo data to check if this is scales
        return sample_list
