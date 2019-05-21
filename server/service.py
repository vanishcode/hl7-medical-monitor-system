# -*- coding: utf-8 -*-
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))  # 创建一个连接
channel = connection.channel()  # 建立通道

# 清除队列，再新建
channel.queue_delete(queue='hello')
channel.queue_declare(queue='hello')  # 把消费者和queue绑定起来，生产者和queue的也是hello


def callback(ch, method, properties, body):  # 回调函数get消息体
    print(" [x] Received %r" % body)


channel.basic_consume('hello', callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()  # 创建死循环，监听消息队列，可使用CTRL+C结束监听
