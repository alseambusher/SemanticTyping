__author__ = 'alse'
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cosine


def tfidf(train_examples, test_examples):
    vectorizer = TfidfVectorizer()
    data = [" ".join(train_examples), " ".join(test_examples)]
    value = vectorizer.fit(data).toarray()
    return cosine(value[0], value[1])


def soft_tfidf(train_examples, test_examples):
    pass


# TODO
def get_abbr_patterns(abbr):
    abbr = re.sub(r'\p{P}', "", abbr)
    return []


def abbr_test(train_examples, test_examples):
    # TODO if test_examples is a string, perform metadata abbr test (label thing). Else do the normal one
    if isinstance(test_examples, str):
        pass
    else:
        pass
    if len(test_examples) > 200:
        return 0.0

