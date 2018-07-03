# -*- coding: utf-8 -*-
from pyspark import *
import os

sc = SparkContext("local")
rdd = sc.parallelize("hello Pyspark world".split(" "))
counts = rdd \
    .flatMap(lambda line: line) \
    .map(lambda word: (word, 1)) \
    .reduceByKey(lambda a, b: a + b)
counts.saveAsTextFile("wc")
sc.stop


