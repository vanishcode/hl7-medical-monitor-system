# -*- coding: utf-8 -*-
"""
desc: 客户端接受响应
last modified: 2019.5.21
"""
import pika
# *localhost 换公网ip
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))  # 创建一个连接
channel = connection.channel()  # 建立通道

# 清除队列，再新建
channel.queue_delete(queue='server_send')
channel.queue_declare(queue='server_send')  # 把消费者和queue绑定起来，生产者和queue的也是hello


def callback(ch, method, properties, body):  # 回调函数get消息体
    print(" [x] Received %r" % body)


channel.basic_consume('server_send', callback)

channel.start_consuming()
