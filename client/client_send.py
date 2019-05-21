# -*- coding: utf-8 -*-
"""
desc: 客户端发送端
last modified: 2019.5.21
"""
import pika
# *localhost 换公网ip
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))  # 创建一个连接
channel = connection.channel()  # 创建通道

# 一次请求
# 请求都为字符串（流），根据字符不同进行不同任务！=_=
channel.queue_declare(queue='server_recv')  # 把消息队列的名字为hello

channel.basic_publish(exchange='',
                      routing_key='server_recv',
                      body='from client')  # 设置routing_key（消息队列的名称）和body（发送的内容）

connection.close()  # 关闭连接
