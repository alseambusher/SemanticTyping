import re

from main import sc

__author__ = 'minh'


class Utils:
    def __init__(self):
        pass

    not_allowed_chars = '[\/*?"<>|\s\t]'
    numeric_regex = r"\A((\\-)?[0-9]{1,3}(,[0-9]{3})+(\\.[0-9]+)?)|((\\-)?[0-9]*\\.[0-9]+)|((\\-)?[0-9]+)|((\\-)?[0" \
                    r"-9]*\\.?[0-9]+([eE][-+]?[0-9]+)?)\Z"

    @staticmethod
    def is_number(example):
        matches = re.match(Utils.numeric_regex, example.strip())
        if matches and matches.span()[1] == len(example.strip()):
            return True
        return False

    @staticmethod
    def clean_examples_numeric(examples):
        return sc.parallelize(examples).map(lambda x: float(x) if Utils.is_number(x) else "").filter(
                lambda x: x).collect()

    @staticmethod
    def get_distribution(data):
        return sc.parallelize(data).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b).sortBy(
            lambda x: x).zipWithIndex().flatMap(lambda value, idx: [str(idx)] * int(value/len(data) * 100))

    @staticmethod
    def get_index_name(index_config):
        return "%s!%s" % (index_config['name'], index_config['size'])
