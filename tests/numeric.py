import random
from scipy.stats import mannwhitneyu, f_oneway, ks_2samp

__author__ = 'alse'


def kolmogorov_smirnov_test(train_examples, test_examples):
    sample1 = random.sample(test_examples, 100 if len(test_examples) > 100 else len(test_examples))
    sample2 = random.sample(train_examples, 100 if len(train_examples) > 100 else len(train_examples))
    if len(sample1) > 1 and len(sample2) > 1:
        return ks_2samp(sample1, sample2)
    return 0.0


def mann_whitney_u_test(train_examples, test_examples):
    if len(train_examples) > 1 and len(test_examples) > 1:
        return mannwhitneyu(train_examples, test_examples).pvalue
    return 0.0


def mann_whitney_num_test(train_examples, test_examples):
    return mann_whitney_u_test(train_examples, test_examples)


def anova_test(train_examples, test_examples):
    if len(train_examples) > 1 and len(test_examples) > 1:
        return f_oneway(train_examples, test_examples).pvalue
    return 0.0
