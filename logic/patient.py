# -*- coding: utf-8 -*-

import os
import sqlite3


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
    return res


def insertdata():
    pass


def updatedata():
    pass


def deletedata(unumber):
    pass
# getdata(unumber='p1')
