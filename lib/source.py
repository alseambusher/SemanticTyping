__author__ = 'alse'
import json
import csv
import xml.etree.ElementTree as ET
from column import Column


class Source:
    def __init__(self, name):
        self.name = name
        self.column_map = {}

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_column_map(self):
        return self.column_map

    def save(self, db, folder_path):
        pass

    def read_semantic_type_json(self, file_path):
        data = json.load(file_path)
        node_array = data["graph"]["nodes"]

        for node in node_array:
            semantic_object = node["userSemanticTypes"]
            if semantic_object:
                name = node["columnName"]
                domain = semantic_object[0]["domain"]["uri"]
                type = semantic_object[0]["type"]["uri"]
                self.column_map[name] = domain + "---" + type

    def read_data_from_csv(self, file_path):  # TODO what if there is no header
        with open(file_path) as csv_file:
            reader = csv.DictReader(csv_file)
            headers = reader.fieldnames()
            for header in headers:
                self.column_map[header] = Column(header)

            for row in reader:
                for header in row.iterkeys():
                    self.column_map[header].add_value(row[header])

    def read_data_from_json(self, file_path):
        json_array = json.load(file_path)
        for node in json_array:
            for field in node.keys():
                if field not in self.column_map:
                    column = Column(field)
                    self.column_map[field] = column
                if isinstance(json[field], list):
                    self.column_map[field].valueList.extend(node[field])
                else:
                    self.column_map[field].valueList.append(node[field])

    def read_data_from_xml(self, file_path):
        xml_tree = ET.parse(file_path)
        root = xml_tree.getroot()
        for child in root:
            for attrib_name in child.attrib.keys():
                if attrib_name not in self.column_map:
                    column = Column(attrib_name)
                    self.column_map[attrib_name] = column
                self.column_map[attrib_name].append(child.attrib[attrib_name])
