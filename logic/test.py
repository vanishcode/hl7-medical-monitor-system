# -*- coding: utf-8 -*-

import os
import sqlite3

db_file = os.path.join(os.path.dirname(__file__), '../data/data.db')
# if os.path.isfile(db_file):
#     os.remove(db_file)

# 初始数据:
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# cursor.execute(
#     'create table doctor(id varchar(20) primary key, name varchar(20))')
# cursor.execute(r"insert into user values ('A-001', 'Adam', 95)")
# cursor.execute(r"insert into user values ('A-002', 'Bob', 95)")

# cursor.execute(r"delete from user where name='Bob'")

# cursor.execute(r"update user set name='wjh' where score=95")
# cursor.execute(
#     r"insert into patient values ('p2','d1', '李四','F','30','17863136666','上海市政府','老二','海鲜过敏','精神病','心脏病','不正常')")

result = cursor.execute(r"select * from patient where doctor='d1'").fetchall()

print(result)

cursor.close()
conn.commit()
conn.close()
