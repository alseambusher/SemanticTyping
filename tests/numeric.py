__author__ = 'alse'
from scipy.stats import kstest
from pyspark.mllib.stat import Statistics
import random
from scipy.stats import mannwhitneyu, f_oneway, ks_2samp

def KolmogorovSmirnovTest(trainExamples, testExamples, sc):
    sample1 = sc.parallalize(random.sample(testExamples, 100 if len(testExamples) > 100 else len(testExamples)))
    sample2 = sc.parallalize(random.sample(trainExamples, 100 if len(trainExamples) > 100 else len(trainExamples)))
    if len(sample1) > 1 and len(sample2) > 1:
        return ks_2samp(sample1, sample2)
        #return Statistics.kolmogorovSmirnovTest(sample1, "norm", 0, 1).pValue
    return 0.0


def MannWhitneyUTest(trainExamples, testExamples, sc):
    if len(trainExamples) > 1 and len(testExamples) > 1:
        return mannwhitneyu(trainExamples, testExamples).pvalue
    return 0.0


def MannWhitneyNumTest(trainExamples, testExamples, sc):
    return MannWhitneyUTest(trainExamples, testExamples, sc)


def AnovaTest(trainExamples, testExamples, sc):
    if len(trainExamples) > 1 and len(testExamples) > 1:
        return f_oneway(trainExamples, testExamples).pvalue
    return 0.0




