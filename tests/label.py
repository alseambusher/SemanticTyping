__author__ = 'alse'
import re

def ContentLengthTest(trainMetas, testExamples):
    maxLength = 0.0
    minLength = 1000.0

    for metadata in trainMetas:
        if maxLength < metadata.length * 1.0 / metadata.size:
            maxLength = metadata.length * 1.0 / metadata.size
        if minLength > metadata.length * 1.0 / metadata.size:
            minLength = metadata.length * 1.0 / metadata.size

    avgLength = (minLength + maxLength) / 2

    sumLength = 0

    for example in testExamples:
        sumLength += len(re.split(r'\\s+', example))  # TODO test this

    return abs(sumLength * 1.0 / len(testExamples) - avgLength)


def jaccard_similarity(x,y):
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality/float(union_cardinality)


def LabelTextTest(trainMetas, testLabel):  # TODO check if this is right
    return max([jaccard_similarity(x.label.split(), testLabel.split()) for x in trainMetas])


