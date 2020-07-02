# -*- coding: utf-8 -*-
from pykafka import KafkaClient
from pykafka.common import OffsetType
from itertools import islice
import math
import logging as log

#kafka  的ip和端口
host = '127.0.0.1:9092'
#连接kafka
#log.basicConfig(level=log.DEBUG)
client = KafkaClient(hosts=host)
#展示kafka的可用topic
client.topics


def send(mytopic,message):
    #出错时打印调试日志
    #log.basicConfig(level=log.DEBUG)
    '''生产者'''
    kafka_topic = client.topics[mytopic]
    producer = kafka_topic.get_producer()
    producer.produce(bytes(message))
    producer.stop()

def get(mytopic,n):
    # 消费者
    kafka_topic = client.topics[mytopic]
    #consumer_timeout_ms表示多少ms内没有接收到数据就停止
    consumer = kafka_topic.get_simple_consumer(
        # consumer_group = "test",
        consumer_timeout_ms = 500,
        auto_offset_reset=OffsetType.LATEST,
        # auto_offset_reset=OffsetType.EARLIEST,
        reset_offset_on_start = True
        )
    #copy from Internet,it can output the lastest message!
    MAX_PARTITION_REWIND = 3
    LAST_N_MESSAGES = n
    MAX_PARTITION_REWIND = int(math.ceil(LAST_N_MESSAGES / len(consumer._partitions)))
    offsets = [(p, op.last_offset_consumed - MAX_PARTITION_REWIND)
           for p, op in consumer._partitions.iteritems()]
    offsets = [(p, (o if o > -1 else -2)) for p, o in offsets]
    consumer.reset_offsets(offsets)
    for message in islice(consumer,MAX_PARTITION_REWIND):
    # for message in consumer:
        if message is not None:
            print("-"*200)
            # print(message.offset, message.value)
            print(message.offset,message.value)


if __name__ == '__main__':
    body={"type": "test","src": "test"}
    #发送kafka
    # send('test',body)
    #获取kafka信息
    get('test',1)

    






