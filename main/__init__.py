import os

from pyspark import SparkContext

sc = SparkContext()

root_dir = os.path.abspath(os.path.join(os.path.realpath(__file__), '..'))
data_dir = os.path.join(root_dir, "data/datasets")
train_model_dir = os.path.join(root_dir, "data/train_models")
