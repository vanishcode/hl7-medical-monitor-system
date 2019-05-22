# -*- coding: utf-8 -*-
"""
desc: 服务端接收并响应端
last modified: 2019.5.21
"""

import pika
import re
import sys
from logic import login
from urllib import parse


class Server:
    def __init__(self):

        # *localhost换成0.0.0.0不只限于监听本地
        connection = self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))  # 创建一个连接
        channel = self.channel = connection.channel()  # 建立通道

        # 清除队列，再新建
        channel.queue_delete(queue='server_recv')
        channel.queue_declare(
            queue='server_recv')  # 把消费者和queue绑定起来，生产者和queue的也是

        def callback(ch, method, properties, body):  # !回调函数，在这里处理逻辑并返回
            # body是命令及数据字符串
            message = parse.parse_qs(self.decode_char(body))
            action = message['action'][0]
            res = ''
            if action == 'login':
                res = self.login(message)
            else:
                pass
            self.sendres(res)

        self.channel.basic_consume('server_recv', callback)

        self.channel.start_consuming()  # 创建死循环，监听消息队列，可使用CTRL+C结束监听

    def login(self, message):
        return login.login(
            self, message['uname'][0], message['unumber'][0], message['uid'][0])

    def sendres(self, res):
        self.channel.queue_delete(queue='server_send')
        self.channel.queue_declare(queue='server_send')
        self.channel.basic_publish(
            exchange='', routing_key='server_send',
            body=str(res))  # 设置routing_key（消息队列的名称）和body（发送的内容）

    def decode_char(self, *args):
        response = args[0]
        return response.decode('utf8')


def main():
    sv = Server()


if __name__ == '__main__':
    main()
