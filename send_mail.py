#!/usr/bin/python3
# -*-codig=utf8-*
import pymysql
import sys
import time
from itertools import chain
from conf import *
import email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

###### global  ######
db = pymysql.connect(database_host, database_user, database_passwd ,database_db, charset="utf8")
cursor = db.cursor()

task_id = int(sys.argv[1])
###### global  ######

def update_errorlog(log):
    time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    log = log.replace("'", "\\'")
    sql = "UPDATE %s set errorlog=CONCAT(IFNULL(errorlog, ''), '[%s] %s') where task_id=%d;" % (reportlink_table, time_str, log, task_id)
    print(sql)
    cursor.execute(sql)
    data = cursor.fetchone()
    print(data)
    try:
        db.commit()
    except Exception as err:
        print('[update_errorlog:%s]' % err)
    return data

def update_table(tablename, data, condition):
    update_str = r'`'
    for (k, v) in data.items():
        v = str(v)
        v = v.replace("'", '&#039;')
        update_str += (k + r"`='" + v + r"',`")
    update_str = update_str[:-2]
    sql = 'UPDATE %s SET %s WHERE %s' % (tablename, update_str, condition)
    #print(sql)   
    try:
        exec_result = cursor.execute(sql)
        db.commit()
        return 0
    except Exception as err:
        db.rollback()
        print("[update_table]:%s" % err)
        return -1

def check_status(report_id):
    mail_mission = []
    cursor.execute("SELECT mission_id FROM %s where need_mail=1 and task_id=%d" % (reportlink_table, report_id))
    mail_mission = cursor.fetchall()
    mail_list =list(chain.from_iterable(mail_mission))
    mail_list_new = list(set(mail_list))
    ready_mail = [0]
    for i in range(0,len(mail_list_new)):
        cursor.execute("SELECT count(*) FROM %s where mission_id=%d" % (task_table, int(mail_list_new[i])))
        ready_mail = list(chain.from_iterable(cursor.fetchall()))
    return[len(mail_list), ready_mail[0], mail_list_new]


def send_mail(_user,_pwd,_to,report_id, mission_id_list):
    msg = MIMEMultipart('related')
    msg['Subject'] = "沙盒系统检测" #邮件的标题
    #msg['Subject'] = sub
    msg['From'] = _user
    msg['To'] = ','.join(_to)

#    cursor.execute("SELECT monitor_link FROM %s where need_mail=1 and task_id=%d" % (reportlink_table, report_id))
    
    ready_mail = [0]
    result_list = []
    #for i in range(0,len(mission_id_list)):
    str1 = 'http://10.144.96.115:5555/sandbox_report/mission_list/' + str(mission_id_list[0])
    cursor.execute("SELECT id,fail_reason FROM %s where mission_id=%d" % (task_table, mission_id_list[0]))
    ready_mail = list(chain.from_iterable(cursor.fetchall()))
    #print(type("\n".join('%s' %id for id in ready_mail)))
    
    body=MIMEText(str1, 'HTML', 'gbk')

    msg.attach(body)
    #msg.attach(answer)
    #发送邮件
    s = smtplib.SMTP()
    s.connect("mail.sogou-inc.com")
    s.login(_user,_pwd)  # 登录邮箱的账户和密码
    s.sendmail(_user,_to, msg.as_string())#发送邮件
    s.quit()


def main():
    _usr="qa_svnreader@sogou-inc.com"
    _pwd="New$oGou4U!"
#        #_to=['liuwei213289@sogou-inc.com','malu@sogou-inc.com','yinjingjing@sogou-inc.com']
    _to=['liuyangsi2810@sogou-inc.com']
   
    mail_result =[]
    mail_result = check_status(task_id)
    print(mail_result)
    
    if mail_result[0] == mail_result[1]:
        if mail_result[0] != 0:
            if mail_result[2] == []:
                update_errorlog("mission_id is null\n")
                update_table(reportlink_table, {'need_mail':'2'}, ("task_id=%d" % task_id))
                return -1
            else:
                send_mail(_usr, _pwd, _to, task_id, mail_result[2])
                print('send_mail')
                update_table(reportlink_table, {'need_mail':'2'}, ("task_id=%d" % task_id))
                
        else:
            update_errorlog("No task is need to report\n")
            update_table(reportlink_table, {'need_mail':'2'}, ("task_id=%d" % task_id))
            return -1
            
    else:
        if mail_result[2] == []:
            update_errorlog("the number of tasks is unequal and mission_id is null\n")
            update_table(reportlink_table, {'need_mail':'2'}, ("task_id=%d" % task_id))
            return -1
        else:
            update_errorlog("There are still unfinished tasks, pls wait\n")
            update_table(reportlink_table, {'need_mail':'2'}, ("task_id=%d" % task_id))
            return -1 

    return 0


if __name__ == "__main__":
    main()
