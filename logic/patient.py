# -*- coding: utf-8 -*-

import os
import sqlite3
from logic import str2hl7


def getdata(self, unumber):

    db_file = os.path.join(os.path.dirname(__file__), '../data/data.db')

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    result = cursor.execute(
        r"select * from patient where id='" + unumber + "'").fetchall()
    res = None

    cursor.close()
    conn.commit()
    conn.close()

    if (result and len(result) > 0):
        res = result[0]
        return str2hl7.toHL7(self, res[0], res[1], res[2], res[3], res[4], res[5], res[6], res[7], res[8], res[9], res[10], res[11])
    else:
        return '-1'


def insertdata(self, unumber, data):

    print(data)
    db_file = os.path.join(os.path.dirname(__file__), '../data/data.db')

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    result = cursor.execute(
        "insert into patient values ('" + data['pnumber'][0] + "','" + unumber + "', '" + data['pname'][0] + "','" + data['gender'][0] + "','" + data['yearold'][0] + "','" + data['phone'][0] + "','" + data['home'][0] + "','" + data['job'][0] + "','" + data['allergy'][0] + "','" + data['family_medical_history'][0] + "','" + data['personal_medical_history'][0] + "','无')")

    cursor.close()
    conn.commit()
    conn.close()

    return '0'

# 修改


def updatedata(self, unumber, data):
    db_file = os.path.join(os.path.dirname(__file__), '../data/data.db')

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # 编号 负责医生 姓名 性别 年龄 联系方式 家庭住址 职业 过敏史 家族病史 个人病史 体检记录
    # cursor.execute(
    #     '''create table patient(id varchar(10) primary key, doctor varchar(10), name varchar(20),
    #     gender varchar(2), yearold varchar(2), phone varchar(10),
    #     home varchar(30), job varchar(10), allergy varchar(20),
    #     family_medical_history varchar(20), personal_medical_history varchar(20),
    #     check_record varchar(20))''')message['unumber'][0]

    # 更新语句
    # print(data)
    # cursor.execute(r"update patient set name='" +
    #                data['name'][0] + "' where id='" + unumber + "'")

    cursor.execute(r"update patient set name='" +
                   data['name'][0] + "' where id='" + unumber + "'")
    cursor.execute(r"update patient set gender='" +
                   data['gender'][0] + "' where id='" + unumber + "'")
    cursor.execute(r"update patient set yearold='" +
                   data['yearold'][0] + "' where id='" + unumber + "'")
    cursor.execute(r"update patient set job='" +
                   data['job'][0] + "' where id='" + unumber + "'")
    cursor.execute(r"update patient set phone='" +
                   data['phone'][0] + "' where id='" + unumber + "'")
    cursor.execute(r"update patient set family_medical_history='" +
                   data['family'][0] + "' where id='" + unumber + "'")
    cursor.execute(r"update patient set allergy='" +
                   data['allergy'][0] + "' where id='" + unumber + "'")
    cursor.close()
    conn.commit()
    conn.close()

    return '0'


def deletedata(self, unumber):
    db_file = os.path.join(os.path.dirname(__file__), '../data/data.db')

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    result = cursor.execute(
        r"delete from patient where id='" + unumber + "'").fetchall()
    cursor.close()
    conn.commit()
    conn.close()

    if len(result) == 0:
        return '-1'
    else:
        return '0'


def getemperature(self, unumber, date, graphtype):
    db_file = os.path.join(os.path.dirname(__file__), '../data/data.db')

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    result = cursor.execute(
        r"select * from " + graphtype + " where id='" + unumber + "' and date='" + date + "'").fetchall()
    res = None
    if (result and len(result) > 0):
        res = result[0]

    cursor.close()
    conn.commit()
    conn.close()

    return res

# 医生用


def getall(self, unumber):
    # unumber 这里指医生的id，找出所有此医生名下的病人
    db_file = os.path.join(os.path.dirname(__file__), '../data/data.db')

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    result = cursor.execute(
        r"select * from patient where doctor='" + unumber + "'").fetchall()

    cursor.close()
    conn.commit()
    conn.close()

    if (result and len(result) > 0):
        return result
    else:
        return '-1'
