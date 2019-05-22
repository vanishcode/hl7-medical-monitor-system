# -*- coding: utf-8 -*-
'''
用户没有db的第一次初始化
'''
import os
import sqlite3


def InitDB():
    # 创建db文件
    db_file = os.path.join(os.path.dirname(__file__), '../data/data.db')
    if os.path.isfile(db_file):
        os.remove(db_file)

    # 初始化表数据:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    # doctor
    cursor.execute(
        'create table doctor(id varchar(10) primary key, name varchar(20))')
    # 测试数据
    cursor.execute(r"insert into doctor values ('a1', '杨永信')")

    # patient
    # 编号 姓名 性别 年龄 联系方式 家庭住址 职业 过敏史 家族病史 个人病史 体检记录
    cursor.execute(
        '''create table patient(id varchar(10) primary key, name varchar(20),
        gender varchar(2), yearold varchar(2), phone varchar(10),
        home varchar(30), job varchar(10),allergy varchar(20),
        family_medical_history varchar(20), personal_medical_history varchar(20),
        check_record varchar(20))''')
    # temperature
    cursor.execute(
        '''create table temperature(id varchar(10) primary key, date varchar(10), 
        clock0 int, clock2 int, clock4 int, clock6 int, clock8 int, 
        clock10 int, clock12 int, clock14 int, clock16 int, 
        clock18 int, clock20 int, clock22 int)''')
    # pulse
    cursor.execute(
        '''create table pulse(id varchar(10) primary key, date varchar(10), 
        clock0 int, clock2 int, clock4 int, clock6 int, clock8 int, 
        clock10 int, clock12 int, clock14 int, clock16 int, 
        clock18 int, clock20 int, clock22 int)''')
    # heart
    cursor.execute(
        '''create table heart(id varchar(10) primary key, date varchar(10), 
        clock0 int, clock2 int, clock4 int, clock6 int, clock8 int,
         clock10 int, clock12 int, clock14 int, clock16 int, 
         clock18 int, clock20 int, clock22 int)''')
    cursor.close()
    conn.commit()
    conn.close()


# InitDB()
