__author__ = 'alse'


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

    sum_length += len(" ".join(test_examples).split())

    return abs(sum_length * 1.0 / len(test_examples) - avg_length)


def jaccard_similarity(x, y):
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality / float(union_cardinality)


def get_n_grams(sentence, n):
    return [sentence[i:i + n] for i in xrange(len(sentence) - n)]


def label_text_test(train_metas, test_label):  # TODO check if this is right
    return max([jaccard_similarity(get_n_grams(x, 2), get_n_grams(test_label, 2)) for x in train_metas])
