# -*- coding: utf-8 -*-
"""
时间转换工具
"""
import time

dt = "2019-05-05 20:28:54"

# 转换成时间数组
timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
# 转换成时间戳
timestamp = time.mktime(timeArray)

time_local = time.localtime(timestamp)

dt1 = time.strftime("%Y-%m-%d %H:%M:%S", time_local)

print(timestamp, dt1)
