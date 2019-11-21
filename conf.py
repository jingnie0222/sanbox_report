#!/usr/bin/python3
#coding=utf-8

import os

script_path = "/search/odin/yinjingjing/python/sandbox_report"

###数据库相关配置
database_host = "10.143.45.197"
database_db = "sand_box"
database_user = "root"
database_passwd = "sogou"

task_table = "sandbox_report_sandboxtask"
reportlink_table = "sandbox_report_sandboxreportlink"
reportvalue_table = "sandbox_report_sandboxreportval"


###平台接口
monitor_ip = "http://sqa.sogou.zw.ted:9999/jarvan/getMonitorResult"

log_file = os.path.join(script_path, "log/autorun.log")



