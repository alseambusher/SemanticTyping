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

    numeric_regex = r"\A((\\-)?[0-9]{1,3}(,[0-9]{3})+(\\.[0-9]+)?)|((\\-)?[0-9]*\\.[0-9]+)|((\\-)?[0-9]+)|((\\-)?[0-9]*" \
                    r"\\.?[0-9]+([eE][-+]?[0-9]+)?)\Z"

    def __init__(self, column_name, true_label, train_examples_map, test_examples, sc):
        self.train_examples_map = train_examples_map
        self.test_examples = test_examples
        self.true_label = true_label
        self.name = column_name
        self.numeric_test_examples = self.clean_examples_numeric(self.test_examples)

        count_numeric = 0
        for example in self.test_examples:
            if IntegratedTest.numeric_regex.match(example):
                count_numeric += 1

        if count_numeric / len(self.test_examples) > 0.7:
            self.is_numeric = True
        else:
            self.is_numeric = False

        self.sc = sc

    def get_all_feature_vectors(self):
        feature_vectors = []
        sb = " ".join(self.test_examples)

        """
            TODO for tfidf score map
            List<SemanticTypeLabel> tfidfResults = new Searcher(new IntegratedTypingHandler("semantic-labeling").getIndexDirectory(2),
            Indexer.CONTENT_FIELD_NAME).getTopK(15, sb.toString());
        """
        for label in self.train_examples_map.keys():
            result_map = {}
            self.test_histogram(label, result_map)
            self.test_numeric(label, result_map)
            self.test_textual(label, result_map)
            self.test_label(label, result_map)

            feature_vectors.append(result_map)

        return feature_vectors

    def test_histogram(self, label, result_map):
        highest_examples = IntegratedTest.get_distribution(self.test_examples)
        result_map[self.ANOVA_TEST] = anova_test(self.train_examples_map[label]['histogram'], highest_examples,
                                                 self.sc)
        result_map[self.MW_TEST] = mann_whitney_num_test(self.train_examples_map[label]['histogram'], highest_examples,
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

    @staticmethod
    def clean_examples_numeric(examples):
        cleaned = []
        for example in examples:
            matches = re.match(IntegratedTest.numeric_regex, example.strip())
            if matches and matches.span()[1] == len(example.strip()):
                cleaned.append(str(float(example.strip())))
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
            sample_list.extend([str(idx)] * int(distribution / len(data) * 100))
            # TODO add pseudo datasets to check if this is scales
        return sample_list
