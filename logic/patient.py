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
    if (result and len(result) > 0):
        res = result[0]

    cursor.close()
    conn.commit()
    conn.close()
    # sqlite
    # id | doctor | name | gender | yearold | phone | home | job | allergy | family_medical_history | personal_medical_history | check_record
    # func
    # idnum, doctor, name, gender, yearold, phone, home, job, allergy, family_medical_history, personal_medical_history, check_record
    return str2hl7.toHL7(self, res[0], res[1], res[2], res[3], res[4], res[5], res[6], res[7], res[8], res[9], res[10], res[11])
    # return res


def insertdata():
    pass


def updatedata():
    pass


def deletedata(unumber):
    pass


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
