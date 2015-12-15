import json
import csv
from xml.etree import ElementTree
from column import Column
from tests.integrated import IntegratedTest

__author__ = 'alse'


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

    def save(self, es, index_config):
        for column_name in self.column_map.keys():
            if self.column_map[column_name].semantic_type:
                doc_body = {
                    'textual': " ".join(self.column_map[column_name].value_list).decode('unicode_escape').encode(
                        'ascii', 'ignore'),
                    'numeric': " ".join(
                            IntegratedTest.clean_examples_numeric(self.column_map[column_name].value_list)),
                    'histogram': " ".join(
                            IntegratedTest.get_distribution(self.column_map[column_name].value_list))}

                es.index(index=('%s!%s' % (index_config['name'], index_config['size'])),
                         doc_type=self.column_map[column_name].semantic_type,
                         body=doc_body)

    def read_semantic_type_json(self, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
            node_array = data["graph"]["nodes"]

            for node in node_array:
                if "userSemanticTypes" in node:
                    semantic_object = node["userSemanticTypes"]
                    name = node["columnName"]
                    domain = semantic_object[0]["domain"]["uri"].split("/")[-1]
                    type = semantic_object[0]["type"]["uri"].split("/")[-1]
                    self.column_map[name].semantic_type = domain + "---" + type

    def read_data_from_csv(self, file_path):  # TODO what if there is no header
        with open(file_path) as csv_file:
            reader = csv.DictReader(csv_file)
            headers = reader.fieldnames
            for header in headers:
                self.column_map[header] = Column(header)

            for row in reader:
                for header in row.iterkeys():
                    self.column_map[header].add_value(row[header])

    def read_data_from_json(self, file_path):
        with open(file_path, 'r') as f:
            json_array = json.load(f)
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
        xml_tree = ElementTree.parse(file_path)
        root = xml_tree.getroot()
        for child in root:
            for attrib_name in child.attrib.keys():
                if attrib_name not in self.column_map:
                    column = Column(attrib_name)
                    self.column_map[attrib_name] = column
                self.column_map[attrib_name].append(child.attrib[attrib_name])
