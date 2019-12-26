#!/usr/bin/python3
# -*-codig=utf8-*

import subprocess
import pymysql
import time
import os
import re
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

def get_task_info():
    sql = "SELECT id, mission_id, module_name, local_path, local_ip, pid, run_time, check_time FROM %s where id='%d'" % (task_table, task_id)
    cursor.execute(sql)
    data = cursor.fetchone()
    db.commit()
    return data

def get_core_result(ip, path, run_time, check_time):
    data = {
        'ip':ip,
        'check_dir':path,
        'starttime':run_time,
        'stoptime':check_time
        }
    #print(data)
    try:
        res = requests.post("http://10.134.36.39:3334/log/check_core", data=data, timeout=50)
        res.encoding = 'utf-8'
        result_str = json.dumps(json.loads(res.text)['data'])
        #print(result_str)
        
        if 'core_file' in result_str:
            result_new = re.findall(r"core_file\":\ \"(.+?)\"\}",result_str)
        #print(result_new)
        return(len(result_new))
    except Exception as err:
        print('[get_core_result] get link is timeout')
        return -1
    
    


def get_qps_result(ip, path, pid, run_time, check_time):
    data = {
        'type':'1',
        'ip':ip,
        'baseDir':path,
        'pid':pid,
        'starttime':run_time,
        'endtime':check_time
        }
    try:
        res = requests.post("http://rsync.sqa.sogou.zw.ted:9999/jarvan/getMonitorResult", data=data, timeout=10)
        res.encoding = 'utf-8'
        result_dict = json.loads(res.text)
        #print("%s" % result_dict)
        key_list = list(result_dict['data'].keys())
        #print(key_list)
        key_list_result = []
        for i in range(0,len(key_list)):
            if 'qps' in key_list[i] and 'Detail' not in key_list[i]:
                key_list_result.append(key_list[i])
        #print(key_list_result)

        if result_dict['code'] != "0":
            print("code:%s\n" % result['code'])
            return -1
        
        link_list=[]
        for i in range(0,len(key_list_result)):
            if result_dict['data'][key_list_result[i]] != '':
                link_list.append(result_dict['data'][key_list_result[i]])
            else:
                update_errorlog("[get_log_result] link:%s\n" % err)
                return -1
        #print(link_list)

    except Exception as err:
        update_errorlog("[get_qps_result] link:%s\n" % err)
        return -1


    ###返回结果为5min平均值
    result = []
    result_str = ''
    result_list = []
    avg_result=[]
    try:
        for i in range(0,len(key_list_result)):
            result.append(requests.post(link_list[i], timeout=10))
            result_str = json.dumps(json.loads(result[i].text)['datas'])
            if 'qps' in key_list_result[i]:
                result_new = re.findall(r"qps\":\ (.+?)\,",result_str)
            if '}' in result_new[0]:
                if 'qps' in key_list_result[i]:
                    result_new = re.findall(r"qps\":\ (.+?)\}\,",result_str)
            #print(result_new)
            result_list = list(map(float, result_new))
            #print(result_list)
            avg_new = round(sum(result_list)/len(result_list),3)
            avg_result.append(avg_new)
    except Exception as err:
        update_errorlog("[get_log_result] data:%s\n" % err)
        return -1

    return("".join('%s' %id for id in avg_result))


def main():
    
    ### get task info
    (id, mission_id, module_name, local_path, local_ip, pid, run_time, check_time) = get_task_info()

    ### get check qps result
    ret_qps = get_qps_result(local_ip, local_path, pid, run_time, check_time)
    print(ret_qps)
    if ret_qps == -1:
        update_table(task_table, {'fail_reason':'get_qps failed'}, ("id=%d" % task_id))
        update_table(task_table, {'is_checked_ok':2}, ("id=%d" % task_id))
        update_table(task_table, {'need_check':2}, ("id=%d" % task_id))
        return -1
    if float(ret_qps) == 0.0:
        update_errorlog("qps is equal to 0\n")
        update_table(task_table, {'fail_reason':'qps is equal to 0'}, ("id=%d" % task_id))
        update_table(task_table, {'is_checked_ok':2}, ("id=%d" % task_id))
        update_table(task_table, {'need_check':2}, ("id=%d" % task_id))
        return -1
    elif float(ret_qps) > 0.0:
        ### get check core result
        core_num = get_core_result(local_ip, local_path, run_time, check_time)
        if core_num > 0:
            update_errorlog("core\n")
            update_table(task_table, {'fail_reason':'core'}, ("id=%d" % task_id))
            update_table(task_table, {'is_checked_ok':2}, ("id=%d" % task_id))
            update_table(task_table, {'need_check':2}, ("id=%d" % task_id))
            return -1
        else:
            ### set finish generate report
            update_table(task_table, {'fail_reason':''}, ("id=%d" % task_id))
            update_table(task_table, {'is_checked_ok':1}, ("id=%d" % task_id))
            update_table(task_table, {'need_check':2}, ("id=%d" % task_id))
            #print("check_task_available.py callable\n")
            return 0
    else:
        update_errorlog("qps is Invalid\n")
        return -1


if __name__ == "__main__":
#    try:
    main()
#    except Exception as e:
#        update_errorlog("%s\n" % e) 
#        set_status(2) 


