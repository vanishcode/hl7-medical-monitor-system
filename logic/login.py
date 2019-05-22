# -*- coding: utf-8 -*-

import os
import sqlite3


def login(self, uname, unumber, uid):
    # print(uname.decode('utf8'), unumber, uid)
    db_file = os.path.join(os.path.dirname(__file__), '../data/data.db')

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    result = cursor.execute(r"select * from " + uid +
                            " where id='" + unumber + "' and name='" + uname + "'").fetchall()
    resnum = -1
    if (result and len(result) > 0):
        # print(result[0][0], result[0][1])
        resnum = 0

    cursor.close()
    conn.commit()
    conn.close()
    return resnum
