#!/usr/bin/python3
# -*-codig=utf8-*
import pymysql
import time
import subprocess
from conf import *

###### global  ######
db = pymysql.connect(database_host, database_user, database_passwd ,database_db, charset="utf8")
cursor = db.cursor()
log_fd = open(log_file, 'w')
###### global  ######

def get_report_id():
    cursor.execute("SELECT id FROM %s where need_report=1 ORDER BY run_time limit 1" % task_table)
    data = cursor.fetchone()
    db.commit()
    if data == None:
        return -1
    print(data[0])
    return data[0]
    

def get_check_id():
    cursor.execute("SELECT id FROM %s where need_check=1 ORDER BY run_time limit 1" % task_table)
    data = cursor.fetchone()
    db.commit()
    if data == None:
        return -1
    print(data[0])
    return data[0]


def main():

    while True:      
        time.sleep(2)
        
        check_id = get_check_id()
        print("check_id:%d" % check_id)
        if check_id != -1:
            subprocess.Popen(['/usr/local/bin/python3', 'check_task_available.py','%d' % check_id], shell = False, stdout = log_fd, stderr = log_fd, cwd=script_path)
        
        report_id = get_report_id()
        print("report_id:%d" % report_id)
        if report_id != -1:
            subprocess.Popen(['/usr/local/bin/python3', 'gen_report.py','%d' % report_id], shell = False, stdout = log_fd, stderr = log_fd, cwd=script_path)



if __name__ == "__main__":
    main()               