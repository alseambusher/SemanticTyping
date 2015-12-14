__author__ = 'alse'


class SemanticLabeler:
    def __init__(self):
        self.source_map = {}
        self.file_writer = open("semantic-labeling.txt", "w")
        self.false_file_writer = open("semantic-labeling-wrong-case.txt", "w")
        self.summary_file_writer = open("semantic-labeling-summary.txt", "w")

    def initialize_attributes(self):
        pass


    def train_random_forest(self):
        pass
