from pyspark import SparkContext
from pyspark.sql import SQLContext

sc = SparkContext()
sqlc = SQLContext(sc)

data_source_format = 'org.apache.hadoop.hbase.spark'

df = sc.parallelize([('a', '1.0'), ('b', '2.0')]).toDF(schema=['col0', 'col1'])

# ''.join(string.split()) in order to write a multi-line JSON string here.
catalog = ''.join("""{
    "table":{"namespace":"default", "name":"testtable"},
    "rowkey":"key",
    "columns":{
        "col0":{"cf":"rowkey", "col":"key", "type":"string"},
        "col1":{"cf":"cf", "col":"col1", "type":"string"}
    }
}""".split())

# Writing
# alternatively: .option('catalog', catalog)
df.write \
    .options(catalog=catalog) \
    .format(data_source_format) \
    .save()

# Reading
df = sqlc.read \
    .options(catalog=catalog) \
    .format(data_source_format) \
    .load()
