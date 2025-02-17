from semantic_labeler import SemanticLabeler
from pyspark import SparkContext


def run_experiments(data_set, sc):
    semantic_labeler = SemanticLabeler(sc)
    semantic_labeler.read_data_sources("datasets/%s" % data_set)
    semantic_labeler.train_semantic_types(list(range(len(semantic_labeler.source_map))))


if __name__ == "__main__":
    sc = SparkContext()
    run_experiments("soccer", sc)