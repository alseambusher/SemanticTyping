import os
from itertools import cycle

from lib.source import Source

__author__ = 'alse'


class SemanticLabeler:
    def __init__(self):
        self.source_list = []
        self.file_writer = open("semantic-labeling.txt", "w")
        self.false_file_writer = open("semantic-labeling-wrong-case.txt", "w")
        self.summary_file_writer = open("semantic-labeling-summary.txt", "w")

    def read_data_sources(self, folder_path):
        data_folder_path = os.path.join(folder_path, "data")
        model_folder_path = os.path.join(folder_path, "model")

        for filename in os.listdir(data_folder_path):
            extension = os.path.splitext(filename)[1]

            source = Source(os.path.splitext(filename[0]))
            file_path = os.path.join(data_folder_path, filename)

            if extension == "csv":
                source.read_data_from_csv(file_path)
            elif extension == "json":
                source.read_data_from_json(file_path)
            elif extension == "xml":
                source.read_data_from_xml(file_path)
            self.source_list.append(source)

        for filename in os.listdir(model_folder_path):
            source = self.source_list[os.path.splitext(filename)[0]]

            source.read_semantic_type_json()

# TODO
    def train_random_forest(self):
        pass

#TODO
    def train_semantic_types(self, size_list):
        for idx, source in enumerate(self.source_list):
            for size in size_list:
                for train_source in cycle(self.source_list)[idx + 1: idx + size + 1]:
                    pass

#TODO
    def test_semantic_types(self):
        pass