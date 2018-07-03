from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


def deal_data(rdd):
    data = rdd.collect()
    for d in data:
        print(d)


sc = SparkContext(sparkHome="local",appName="Realtime-Analytics-Engine")
ssc = StreamingContext(sc, batchDuration=int(6))

kafkaParams = {"metadata.broker.list": "192.168.32.18:9092,192.168.32.19:9092,192.168.32.20:9092",
               "serializer.class": "kafka.serializer.StringEncoder",
               "auto.offset.reset": "smallest",
               "fetch.message.max.bytes": "22388608"}
kvs = KafkaUtils.createDirectStream(ssc, list('senmdt-cache-records'), kafkaParams,
                                    keyDecoder="kafka.serializer.StringEncoder",
                                    valueDecoder="kafka.serializer.StringEncoder")

kvs.foreachRDD(lambda rdd: deal_data(rdd))
