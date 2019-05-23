# -*- coding: utf-8 -*-
"""
desc: 服务端接收并响应端
last modified: 2019.5.21
"""

import pika
import re
import sys
from logic import login
from logic import patient
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

            elif action == 'getdata':
                res = self.getdata(message)
            elif action == 'temperature':
                res = self.getemperature(message, 'temperature')
            elif action == 'pulse':
                res = self.getemperature(message, 'pulse')
            elif action == 'heart':
                res = self.getemperature(message, 'heart')

            # 添加
            elif action == 'add':
                res = self.add(message)

            elif action == 'update':
                res = self.update(message)

            elif action == 'delete':
                res = self.delete(message)

            self.sendres(res)

        self.channel.basic_consume('server_recv', callback)

        self.channel.start_consuming()  # 创建死循环，监听消息队列，可使用CTRL+C结束监听

    def login(self, message):
        return login.login(
            self, message['uname'][0], message['unumber'][0], message['uid'][0])

    def getdata(self, message):
        # body里有`&`可能影响解析
        return patient.getdata(self, message['unumber'][0])

    def getemperature(self, message, graphtype):
        return patient.getemperature(self, message['unumber'][0], message['date'][0], graphtype)
    # 增加

    def add(self, message):
        return patient.insertdata(self, message['unumber'][0], message)

    def update(self, message):
        return patient.updatedata(self, message['unumber'][0], message)

    def delete(self, message):
        return patient.deletedata(self, message['unumber'][0])

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
