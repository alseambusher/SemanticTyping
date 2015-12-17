from semantic_labeler import SemanticLabeler

__author__ = 'alse'


def run_experiments(data_set):
    semantic_labeler = SemanticLabeler()
    semantic_labeler.read_data_sources("datasets/%s" % data_set)
    semantic_labeler.train_semantic_types(list(range(len(semantic_labeler.source_map))))


if __name__ == "__main__":
    run_experiments("soccer")