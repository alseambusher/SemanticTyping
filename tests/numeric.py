__author__ = 'alse'
from pyspark.mllib.stat import Statistics
import random
from scipy.stats import mannwhitneyu, f_oneway, ks_2samp


def kolmogorov_smirnov_test(train_examples, test_examples, sc):
    sample1 = sc.parallalize(random.sample(test_examples, 100 if len(test_examples) > 100 else len(test_examples)))
    sample2 = sc.parallalize(random.sample(train_examples, 100 if len(train_examples) > 100 else len(train_examples)))
    if len(sample1) > 1 and len(sample2) > 1:
        return ks_2samp(sample1, sample2)
        #return Statistics.kolmogorovSmirnovTest(sample1, "norm", 0, 1).pValue
    return 0.0


def mann_whitney_u_test(train_examples, test_examples, sc):
    if len(train_examples) > 1 and len(test_examples) > 1:
        return mannwhitneyu(train_examples, test_examples).pvalue
    return 0.0


def mann_whitney_num_test(train_examples, test_examples, sc):
    return mann_whitney_u_test(train_examples, test_examples, sc)


def anova_test(train_examples, test_examples, sc):
    if len(train_examples) > 1 and len(test_examples) > 1:
        return f_oneway(train_examples, test_examples).pvalue
    return 0.0




