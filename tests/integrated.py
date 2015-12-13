from sympy import content
from tests.label import ContentLengthTest, LabelTextTest
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

    isNumeric = False
    testExamples = []
    textualExampleMap = {}
    histogramExampleMap = {}
    numericExampleMap = {}
    metaExampleMap = {}
    resultMap = {}
    trueLabel = None
    name = None
    tfidfScoreMap = None
    numericRegEx = re.compile("^((\\-)?[0-9]{1,3}(,[0-9]{3})+(\\.[0-9]+)?)|((\\-)?[0-9]*\\.[0-9]+)|((\\-)?[0-9]+)|((\\-)?[0-9]*\\.?[0-9]+([eE][-+]?[0-9]+)?)$")

    def __init__(self, trueLabel, testExamples, textualExampleMap, histogramExampleMap, numericExampleMap, metaExampleMap, isNumeric, sc):
        self.testExamples = testExamples
        self.textualExampleMap = textualExampleMap
        self.histogramExampleMap = histogramExampleMap
        self.numericExampleMap = numericExampleMap
        self.metaExampleMap = metaExampleMap
        self.isNumeric = isNumeric
        self.trueLabel, self.name = trueLabel.split("!")[:2]
        self.sc = sc

    def get_all_feature_vectors(self):
        instanceMap = {}
        sb = " ".join(self.testExamples)
        self.tfidfScoreMap = {}
        """
                TODO for tfidf score map
                List<SemanticTypeLabel> tfidfResults = new Searcher(new IntegratedTypingHandler("semantic-labeling").getIndexDirectory(2),
                Indexer.CONTENT_FIELD_NAME).getTopK(15, sb.toString());
        """
        for label in self.histogramExampleMap:
            self.test_histogram(label)
            self.test_numeric(label)
            self.test_textual(label)
            self.test_label(label)

            instanceMap[self.get_feature_vector()] = "Yes!" + label if label == self.trueLabel else "No!" + label

        return instanceMap

    def get_feature_vector(self):  # TODO
        return None

    def test_histogram(self, label):
        histestExamples = IntegratedTest.get_distribution(self.testExamples)
        self.resultMap[self.KS_TEST] = KolmogorovSmirnovTest(self.numericExampleMap[label], histestExamples, self.sc)
        self.resultMap[self.KS_TEST] = MannWhitneyNumTest(self.numericExampleMap[label], histestExamples, self.sc)


    def test_numeric(self, label):
        if not self.isNumeric or not self.numericExampleMap.has_key(label):
            self.resultMap[self.KS_TEST] = 0.0
            self.resultMap[self.MW_NUM_TEST] = 0.0
        else:
            examples = self.clean_examples_numeric(self.testExamples)  # TODO see if we can do this only once
            self.resultMap[self.KS_TEST] = KolmogorovSmirnovTest(self.numericExampleMap[label], examples, self.sc)
            self.resultMap[self.KS_TEST] = MannWhitneyNumTest(self.numericExampleMap[label], examples, self.sc)

    def test_label(self, label):
        self.resultMap[self.LBL_ABBR_TEST] = abbr_test(self.metaExampleMap[label], self.name)
        self.resultMap[self.LBL_TEST] = LabelTextTest(self.metaExampleMap[label], self.name)
        self.resultMap[self.VALUE_SIZE] = ContentLengthTest(self.metaExampleMap[label], self.name)

    def test_textual(self, label):
        if not self.numericExampleMap.has_key(label):
            self.resultMap[self.SOFT_TFIDF_TEST] = 0.0
            self.resultMap[self.ABBR_TEST] = 0.0
        else:
            self.resultMap[self.SOFT_TFIDF_TEST] = tfidf(self.textualExampleMap[label], self.testExamples)
            self.resultMap[self.ABBR_TEST] = abbr_test(self.textualExampleMap[label], self.testExamples)

    def clean_examples_numeric(self, examples):
        cleaned = []
        for example in examples:
            if self.numericRegEx.match(example.strip()):
                cleaned.append(float(example.strip()))
        return cleaned

    @staticmethod
    def get_distribution(data):
        distribution = {}
        for entry in data:
            if distribution.has_key(entry):
                distribution[entry] += 1
            else:
                distribution[entry] = 1.0

        # TODO add pseudo data to check if this is scales
        return sorted([x/len(data) for x in distribution.values()])

