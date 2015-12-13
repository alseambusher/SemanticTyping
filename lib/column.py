__author__ = 'alse'


class Column:
    def __init__(self, name):
        self.name = name
        self.value_list = []
        self.semantic_type = None

    def add_value(self, value):
        self.value_list.append(value)

    def get_value_list(self):
        return self.value_list

    def set_semantic_type(self, semantic_type):
        self.semantic_type = semantic_type

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name



