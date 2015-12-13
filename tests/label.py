__author__ = 'alse'
import re


def content_length_test(train_metas, test_examples):
    max_length = 0.0
    min_length = 1000.0

    for metadata in train_metas:
        if max_length < metadata.length * 1.0 / metadata.size:
            max_length = metadata.length * 1.0 / metadata.size
        if min_length > metadata.length * 1.0 / metadata.size:
            min_length = metadata.length * 1.0 / metadata.size

    avg_length = (min_length + max_length) / 2

    sum_length = 0

    for example in test_examples:
        sum_length += len(re.split(r'\\s+', example))  # TODO test this

    return abs(sum_length * 1.0 / len(test_examples) - avg_length)


def jaccard_similarity(x,y):
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality/float(union_cardinality)


def label_text_test(train_metas, test_label):  # TODO check if this is right
    return max([jaccard_similarity(x.label.split(), test_label.split()) for x in train_metas])


