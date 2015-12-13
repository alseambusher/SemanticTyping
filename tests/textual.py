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


def get_abbr_patterns(abbr):
    if len(abbr) > 5:
        return []

    abbr = re.sub(r'\p{P}', "", abbr)
    patterns = [r"\b"] * 4
    for char in abbr[:-1]:
        patterns[0] += (char + "[a-z]+\p{Z}+")
        patterns[1] += (char + "[a-z]*")
        patterns[2] += (char + "[a-z]*?\p{Z}")
    patterns[0] += (abbr[-1] + "[a-z]+\b")
    patterns[1] += (abbr[-1] + "[a-z]*\b")
    patterns[2] += (abbr[-1] + "[a-z]*\b")
    patterns[3] += (abbr + "[a-z]+\b")

    for idx, pattern in enumerate(patterns):
        patterns[idx] = re.compile(pattern, re.IGNORECASE)

    return patterns


def abbr_test(train_examples, test_examples):
    # if testExamples is a string, perform metadata abbr test (label thing). Else do the normal one
    train_example_set = set(train_examples)

    countMatches = 0

    if isinstance(test_examples, str):
        patterns = get_abbr_patterns(test_examples)
        for pattern in patterns:
            for train_example in train_example_set:
                if pattern.match(train_example):
                    countMatches += 1
        return countMatches * 2.0 / len(train_example_set)
    else:
        test_example_set = set(test_examples)

        if len(test_example_set) > 200:
            return 0.0

        for test_example in test_example_set:
            patterns = get_abbr_patterns(test_example)
            for pattern in patterns:
                for train_example in train_example_set:
                    if pattern.match(train_example):
                        countMatches += 1
        return countMatches * 2.0 / (len(train_example_set) + len(train_example_set))
