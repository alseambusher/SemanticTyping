from sympy import content
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
    numeric_regex = re.compile("^((\\-)?[0-9]{1,3}(,[0-9]{3})+(\\.[0-9]+)?)|((\\-)?[0-9]*\\.[0-9]+)|((\\-)?[0-9]+)|((\\-)?[0-9]*\\.?[0-9]+([eE][-+]?[0-9]+)?)$")

    def __init__(self, true_label, test_examples, textual_example_map, histogram_example_map, numeric_example_map, meta_example_map, is_numeric, sc):
        self.test_examples = test_examples
        self.textual_example_map = textual_example_map
        self.histogram_example_map = histogram_example_map
        self.numeric_example_map = numeric_example_map
        self.meta_example_map = meta_example_map
        self.is_numeric = is_numeric
        self.true_label, self.name = true_label.split("!")[:2]
        self.sc = sc

    def get_all_feature_vectors(self):
        instance_map = {}
        sb = " ".join(self.test_examples)
        self.tfidf_score_map = {}
        """
                TODO for tfidf score map
                List<SemanticTypeLabel> tfidfResults = new Searcher(new IntegratedTypingHandler("semantic-labeling").getIndexDirectory(2),
                Indexer.CONTENT_FIELD_NAME).getTopK(15, sb.toString());
        """
        for label in self.histogram_example_map:
            self.test_histogram(label)
            self.test_numeric(label)
            self.test_textual(label)
            self.test_label(label)

            instance_map[self.get_feature_vector()] = "Yes!" + label if label == self.true_label else "No!" + label

        return instance_map

    def get_feature_vector(self):  # TODO
        return None

    def test_histogram(self, label):
        highest_examples = IntegratedTest.get_distribution(self.test_examples)
        self.result_map[self.KS_TEST] = kolmogorov_smirnov_test(self.numeric_example_map[label], highest_examples, self.sc)
        self.result_map[self.KS_TEST] = mann_whitney_num_test(self.numeric_example_map[label], highest_examples, self.sc)

    def test_numeric(self, label):
        if not self.is_numeric or not self.numeric_example_map.has_key(label):
            self.result_map[self.KS_TEST] = 0.0
            self.result_map[self.MW_NUM_TEST] = 0.0
        else:
            examples = self.clean_examples_numeric(self.test_examples)  # TODO see if we can do this only once
            self.result_map[self.KS_TEST] = kolmogorov_smirnov_test(self.numeric_example_map[label], examples, self.sc)
            self.result_map[self.KS_TEST] = mann_whitney_num_test(self.numeric_example_map[label], examples, self.sc)

    def test_label(self, label):
        self.result_map[self.LBL_ABBR_TEST] = abbr_test(self.meta_example_map[label], self.name)
        self.result_map[self.LBL_TEST] = label_text_test(self.meta_example_map[label], self.name)
        self.result_map[self.VALUE_SIZE] = content_length_test(self.meta_example_map[label], self.name)

    def test_textual(self, label):
        if not self.numeric_example_map.has_key(label):
            self.result_map[self.SOFT_TFIDF_TEST] = 0.0
            self.result_map[self.ABBR_TEST] = 0.0
        else:
            self.result_map[self.SOFT_TFIDF_TEST] = tfidf(self.textual_example_map[label], self.test_examples)
            self.result_map[self.ABBR_TEST] = abbr_test(self.textual_example_map[label], self.test_examples)

    def clean_examples_numeric(self, examples):
        cleaned = []
        for example in examples:
            if self.numeric_regex.match(example.strip()):
                cleaned.append(float(example.strip()))
        return cleaned

    @staticmethod
    def get_distribution(data):
        distribution = {}
        for entry in data:
            if entry in distribution:
                distribution[entry] += 1
            else:
                distribution[entry] = 1.0

        # TODO add pseudo data to check if this is scales
        return sorted([x/len(data) for x in distribution.values()])

