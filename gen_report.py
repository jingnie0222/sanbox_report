#!/usr/bin/python3
# -*-codig=utf8-*

import subprocess
import pymysql
import time
import os
import sys
import requests
import json
from conf import *


###### global  ######
db = pymysql.connect(database_host, database_user, database_passwd ,database_db, charset="utf8")
cursor = db.cursor()

task_id = int(sys.argv[1])
###### global  ######

def update_errorlog(log):
    time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    log = log.replace("'", "\\'")
    sql = "UPDATE %s set errorlog=CONCAT(IFNULL(errorlog, ''), '[%s] %s') where task_id=%d;" % (reportlink_table, time_str, log, task_id)
    #print(sql)
    cursor.execute(sql)
    data = cursor.fetchone()
    try:
        db.commit()
    except Exception as err:
        print('[update_errorlog:%s]' % err)
    return data

def set_status(stat):
    sql = "UPDATE %s set report_status=%d where task_id=%d;" % (reportlink_table, stat, task_id)
    cursor.execute(sql)
    try:
        db.commit()
    except Exception as err:
        db.rollback()
        print("[set_status:%s] % err")

def get_task_info():
    sql = "SELECT id, mission_id, module_name, local_path, local_ip, pid, run_time, check_time FROM %s where id='%d'" % (task_table, task_id)
    cursor.execute(sql)
    data = cursor.fetchone()
    db.commit()
    return data

def create_report_task(table, task_id, mission_id, module_name, local_path, local_ip, pid, run_time, check_time):
    insert_sql = 'INSERT into %s (task_id, mission_id, module_name, local_path, local_ip, pid, run_time, check_time) VALUES ("%d", "%d", "%s", "%s", "%s", "%s", "%s", "%s")' 
    para = (table, task_id, mission_id, module_name, local_path, local_ip, pid, run_time, check_time)
    try:
        cursor.execute(insert_sql % para)
        db.commit()
        return 0
    except:
        db.rollback()
        update_errorlog("create_report_task failed\n")
        print("create_report_task failed:%s\n" % err)
        return -1
   

def get_monitor_link(ip, path, pid, run_time, check_time):
    data = {
        'type':'0',
        'ip':ip,
        'baseDir':path,
        'pid':pid,
        'starttime':run_time,
        'endtime':check_time
        }
    try:
        res = requests.post(monitor_ip, data=data, timeout=10)
        res.encoding = 'utf-8'
        result = json.loads(res.text)
        print("%s" % result)
        update_errorlog("get monitorlink data:%s\n" % result)
        
        if result['code'] != "0":
            print("code:%s\n" % result['code'])
            return -1
        
        monitor_link = result['data']['pageUrl']
        if not monitor_link:
            print("monitor_link is null\n")
            return -1
        
    except Exception as err:
        update_errorlog("[get_monitor_link]:%s\n" % err)
        return -1
    
    try:
        sql = "UPDATE %s set monitor_link='%s' where task_id=%d" % (reportlink_table, pymysql.escape_string(monitor_link), task_id)
        cursor.execute(sql)
        db.commit()
        return 0
    except Exception as err:
        db.rollback()
        update_errorlog("update monitor_link failed:%s\n" % err)
        print("update monitor_link failed:%s\n" % err)
        return -1
        
        
    
def get_monitor_val():
    pass   
    

def get_script_res():
    pass
    

def main():

    ### get task info
    (id, mission_id, module_name, local_path, local_ip, pid, run_time, check_time) = get_task_info() 
    
    ### create report record 
    ret_creat = create_report_task(reportlink_table, id, mission_id, module_name, local_path, local_ip, pid, run_time, check_time)
    if ret_creat != 0:
        update_errorlog("create_report_task Error, pls check\n")
        set_status(2)
        return -1
    
    ### get monitor link    
    ret_getlink = get_monitor_link(local_ip, local_path, pid, run_time, check_time)
    if ret_getlink != 0:
        update_errorlog("get_monitor_link Error, pls check\n")
        set_status(2)
        return -1
        
    set_status(1)
    return 0

    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        update_errorlog("%s\n" % e) 
        set_status(2)   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    