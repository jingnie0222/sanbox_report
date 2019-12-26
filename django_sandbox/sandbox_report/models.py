from django.db import models

# Create your models here.

#会自动生成一个自增的id字段，在model里不用定义


class SandboxTaskSummary(models.Model):
    mission_id = models.IntegerField(default=-1)
    start_time = models.CharField(max_length=50, blank=True, null=True)
    end_time = models.CharField(max_length=50, blank=True, null=True)
    status = models.IntegerField(default=-1)
    

class SandboxTask(models.Model):
 
    mission_id = models.IntegerField(default=-1)
    module_name = models.CharField(max_length=50, default="")
    is_master = models.IntegerField(default=-1)
    have_update = models.IntegerField(default=-1)
    #-1:初始值；1:需要check；2:check完毕
    need_check = models.IntegerField(default=-1)    
    run_time = models.CharField(max_length=50, default="")
    check_time = models.CharField(max_length=50, default="")  
    #1:成功，2:失败
    is_checked_ok = models.IntegerField(default=-1)
    fail_reason = models.TextField(default="")
    need_rollback = models.IntegerField(default=-1)
    local_path = models.TextField(default="")
    local_ip = models.CharField(max_length=50, default="")
    pid = models.CharField(max_length=50, default="")
    #-1:初始值；1:需要report；2:生成report完毕
    need_report = models.IntegerField(default=-1)
    proc_top_name =  models.CharField(max_length=100, blank=True, null=True)


class SandboxReportLink(models.Model):
    #对应任务表中的主键id
    task_id = models.IntegerField(default=-1)
    
    #对应任务表中的mission_id
    mission_id = models.IntegerField(default=-1)   
    module_name = models.CharField(max_length=50, blank=True, null=True)
    local_path = models.TextField(blank=True, null=True)
    local_ip = models.CharField(max_length=50, blank=True, null=True)
    pid = models.CharField(max_length=50, blank=True, null=True)
    run_time = models.CharField(max_length=50, blank=True, null=True)
    check_time = models.CharField(max_length=50, blank=True, null=True)
    monitor_link = models.TextField(blank=True, null=True)
    script_res = models.TextField(blank=True, null=True)
    #-1:初始值；1:需要mail；2:mail完毕
    need_mail = models.IntegerField(default=-1, null=True)
    #-1:初始值；1:生成报告成功；2:生成报告失败
    report_status = models.IntegerField(default=-1,null=True)
    #-1:初始值；0:无core；1:有core
    is_core = models.IntegerField(default=-1,null=True)
    errorlog = models.TextField(blank=True, null=True)
    
    
class SandboxReportVal(models.Model):
    #对应任务表中的主键id
    task_id = models.IntegerField(default=-1)
    item_name = models.CharField(max_length=50, blank=True, null=True)
    item_min = models.CharField(max_length=20, blank=True, null=True)
    item_max = models.CharField(max_length=20, blank=True, null=True)
    item_avg = models.CharField(max_length=20, blank=True, null=True)
    
    
    
    
    
    
    