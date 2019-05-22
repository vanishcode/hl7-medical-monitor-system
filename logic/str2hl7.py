# -*- coding: utf-8 -*-
'''
str => hl7 str

MSH|^~\&|H01||C13||20190520082206||ORM|2019052008220617041000138810|P|2.4|||NE|AL|CHN|
PID|||000000672850||张三||30|F|||北京市海淀区||17863136044|工程师|||||||||||||||||||||||||||
CDA|||心脏病||花粉过敏|无||正常
ZCS|DIS|DISABLED^^DISABLED^GA^30092|N|DECLINED|DECLINED|08625
# CDA那行是 家族病史 过敏记录 个人病史 体检记录
'''
import time

# 编号 负责医生 姓名 性别 年龄 联系方式 家庭住址 职业 过敏史 家族病史 个人病史 体检记录
# id doctor name gender yearold phone home job allergy family_medical_history personal_medical_history check_record


def toHL7(self, idnum, doctor, name, gender, yearold, phone, home, job, allergy, family_medical_history, personal_medical_history, check_record):
    now = time.strftime("%Y%m%d%H%M%S", time.localtime())
    return 'MSH|^~\&|H01||C13||' + now + '||ORM|' + now + now + '|P|2.4|||NE|AL|CHN|\n' + 'PID||' + doctor + '|'+idnum + '||' + name + '||' + yearold + '|' + gender + '|||' + home + '||' + phone + '|' + job + '|||||||||||||||||||||||||||\n' + 'CDA|||' + allergy + '||' + family_medical_history + '|' + personal_medical_history + '||'+check_record + '\n'+'ZCS|DIS|DISABLED^^DISABLED^GA^30092|N|DECLINED|DECLINED|08625'

# 写入文件


def toHL7file(patient):
    with open('patient.txt', 'w', encoding='utf-8') as f:
        f.write(patient)
