# hl7-medical-monitor-system
基于HL7协议的医疗数据管理系统（C/S）。

## 使用

```bash
pip(3) install -r requirements.txt
# mq
cd rabbitmq_server-3.6.12.902/sbin
# web management
./rabbitmq-plugins
# mq server
./rabbitmq-server
# server
python3 server.py
# client gui
python3 view/login.py
```

## 说明

### 使用的技术栈

Python 3.7.2

wxPython 4.0.4 osx-cocoa (phoenix) wxWidgets 3.0.5

RabbitMQ rabbitmq_server-3.6.12.902

sqllite3

## 协议

Apache License 2.0