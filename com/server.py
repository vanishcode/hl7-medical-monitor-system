# -*- coding: utf-8 -*-
"""
desc: 服务端接收并响应端
last modified: 2019.5.21
"""
import pika


class Server():
    def __init__(self):

        # *localhost换成0.0.0.0不只限于监听本地
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))  # 创建一个连接
        channel = connection.channel()  # 建立通道

        # 清除队列，再新建
        channel.queue_delete(queue='server_recv')
        channel.queue_declare(
            queue='server_recv')  # 把消费者和queue绑定起来，生产者和queue的也是hello

        def callback(ch, method, properties, body):  # 回调函数get消息体
            print(" [x] Received %r" % body)
            # ---------------send-------------
            channel.queue_delete(queue='server_send')
            channel.queue_declare(queue='server_send')  # 把消息队列的名字为hello

            channel.basic_publish(
                exchange='', routing_key='server_send',
                body='from server')  # 设置routing_key（消息队列的名称）和body（发送的内容）

        channel.basic_consume('server_recv', callback)

        channel.start_consuming()  # 创建死循环，监听消息队列，可使用CTRL+C结束监听


def main():
    sv = Server()


if __name__ == '__main__':
    main()