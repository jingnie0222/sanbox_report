from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from sandbox_report.models import SandboxReportLink
from sandbox_report.models import SandboxReportVal
from sandbox_report.models import SandboxTaskSummary
from django.views.decorators.csrf import csrf_exempt
from . import pagination
from . import urlhandle
import re
import collections
# Create your views here.


def url_urlencode(url):
    res = ""
    url_list = re.split(r'[?#]', url)
    print(url_list)
    if len(url_list) < 3:
        return res
        
    params_dict = {}   
    domain = url_list[0]
    params_list = url_list[1].split('&')
    suffix = url_list[2]
    
    for data in params_list:
        key = data.split('=')[0]
        if key == 'starttime' or key == 'endtime':
            value = urlhandle.urlencode(data.split('=')[1], 'utf8', 'ignore')
        else:
            value = data.split('=')[1]
        params_dict[key] = value
        
    res = res + domain + "?" 
    for key,value in params_dict.items():        
        res = res + "&" + key + "=" + value
    res = res + "#" + suffix
    
    return res
   
@csrf_exempt  
def mission_list(request):
        
    if request.method == 'GET':
        page_id = request.GET.get('page','')
        if page_id == '':
            current_page = 1
        else:
            current_page = int(page_id)
        print('current_page',current_page)
        allTast = SandboxTaskSummary.objects.order_by('-mission_id')
        page_obj = pagination.Page(current_page, len(allTast), 5, 10)
        data = allTast[page_obj.start:page_obj.end]
        page_str = page_obj.page_str("?page=")
        #print(page_str)
        return_dict = {
            'li':data,
            'page_str':page_str,
        }

    else:
        return_dict = {
            'li':'',
            'page_str':'',
        }    
    return render(request,'sandbox_report/mission_list.html', return_dict)

@csrf_exempt  
def mission_list_detail(request, missionid):
    if request.method == 'GET':
        # print(missionid)
        task_list = SandboxReportLink.objects.filter(mission_id=missionid)

        return_dict = {
            'task_list': task_list,
        }
    else:
        return_dict = {
            'task_list': ''
        }
    return render(request, 'sandbox_report/mission_list_detail.html', return_dict)
    
    
@csrf_exempt   
def per_mission_detail(request, missionid, taskid):
    if request.method == 'GET':
        val_lst = SandboxReportVal.objects.filter(task_id=taskid)
        val_dict = collections.OrderedDict()
        for val in val_lst:
            key = val.item_name
            value = [val.item_min, val.item_max, val.item_avg]
            val_dict[key] = value
            
        task = SandboxReportLink.objects.filter(task_id=taskid).order_by('-mission_id')[0]
        if task.monitor_link:
                task.monitor_link = url_urlencode(task.monitor_link)
        
        return_dict = {
            'val_dict': val_dict,
            'monitor_link': task.monitor_link,
            'missionid':missionid,
            'ip':task.local_ip,
            'path':task.local_path,
        }
        
    else:
        return_dict = {
            'val_dict': '',
            'monitor_link': '',
            'missionid':missionid,
        }
    print(return_dict)
    return render(request, 'sandbox_report/per_mission_detail.html', return_dict)
        
    
    
    
    
    
    
    
    
    
    
    