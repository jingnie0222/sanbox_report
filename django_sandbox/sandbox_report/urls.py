#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import re_path
from django.urls import path
from . import views

app_name = 'sandbox_report'
urlpatterns = [
    # debug
    path('mission_list/', views.mission_list),
    path('mission_list/<int:missionid>/', views.mission_list_detail),
    path('mission_list/<int:missionid>/<int:taskid>/', views.per_mission_detail),
    # re_path(r'^task_detail$', views.task_detail),
    # re_path(r'^diff_detail$', views.diff_detail),
    # re_path(r'^set_cancel$', views.set_cancel),
    # re_path(r'^re_add$', views.re_add)
]
