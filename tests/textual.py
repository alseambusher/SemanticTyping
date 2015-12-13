__author__ = 'alse'
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cosine


def tfidf(trainExamples, testExamples):
    vectorizer = TfidfVectorizer()
    data = [" ".join(trainExamples), " ".join(testExamples)]
    value = vectorizer.fit(data).toarray()
    return cosine(value[0], value[1])


def soft_tfidf(trainExamples, testExamples):
    pass


# TODO
def get_abbr_patterns(abbr):
    abbr = re.sub(r'\p{P}', "", abbr)
    return []


def abbr_test(trainExamples, testExamples):
    # TODO if testExamples is a string, perform metadata abbr test (label thing). Else do the normal one
    if isinstance(testExamples, str):
        pass
    else:
        pass
    if len(testExamples) > 200:
        return 0.0

