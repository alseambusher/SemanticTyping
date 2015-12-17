import re

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
        if matches and len(matches.span()[1]) == len(example.strip()):
            return True
        return False

    @staticmethod
    def clean_examples_numeric(examples):
        cleaned = []
        for example in examples:
            matches = re.match(Utils.numeric_regex, example.strip())
            if matches and len(matches.span()[1]) == len(example.strip()):
                cleaned.append(str(float(example.strip())))
        return cleaned

    @staticmethod
    def get_distribution(data):
        distribution_map = {}
        for entry in data:
            if entry in distribution_map:
                distribution_map[entry] += 1
            else:
                distribution_map[entry] = 1.0

        sample_list = []
        for idx, distribution in enumerate(sorted(distribution_map.values())):
            sample_list.extend([str(idx)] * int(distribution / len(data) * 100))
            # TODO add pseudo datasets to check if this is scales
        return sample_list

    @staticmethod
    def get_index_name(index_config):
        return "%s!%s" % (index_config['name'], index_config['size'])