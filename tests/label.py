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


def LabelTextTest(trainMetas, testLabel):  # TODO
    pass
