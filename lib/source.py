__author__ = 'alse'
import json
import csv
from column import Column


class Source:
    def __init__(self, name):
        self.name = name
        self.columnMap = {}

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_column_map(self):
        return self.columnMap

    def read_semantic_type_json(self, file_path):
        data = json.load(file_path)
        node_array = data["graph"]["nodes"]

        for node in node_array:
            semantic_object = node["userSemanticTypes"]
            if semantic_object:
                name = node["columnName"]
                domain = semantic_object[0]["domain"]["uri"]
                type = semantic_object[0]["type"]["uri"]
                self.columnMap[name] = domain + "---" + type

    def read_data_from_csv(self, file_path):  # TODO what if there is no header
        with open(file_path) as csvfile:
            reader = csv.DictReader(csvfile)
            headers = reader.fieldnames()
            for header in headers:
                self.columnMap[header] = Column(header)

            for row in reader:
                for header in row.iterkeys():
                    self.columnMap[header].add_value(row[header])
