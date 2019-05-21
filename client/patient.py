# -*- coding: utf-8 -*-
"""
desc: 客户端命令行版本
last modified: 2019.5.21
"""
#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))  # 创建一个连接
channel = connection.channel()  # 创建通道

# 一次请求
# 请求都为字符串（流），根据字符不同进行不同任务！=_=
channel.queue_declare(queue='hello')  # 把消息队列的名字为hello

channel.basic_publish(exchange='', routing_key='hello',
                      body='client')  # 设置routing_key（消息队列的名称）和body（发送的内容）
print(" [x] Sent 'Hello World!'")
# channel.queue_delete(queue='hello')
# channel.queue_purge(queue='hello')
connection.close()  # 关闭连接
