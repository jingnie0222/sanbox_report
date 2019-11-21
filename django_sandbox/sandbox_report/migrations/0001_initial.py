# Generated by Django 2.1.1 on 2019-11-19 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SandboxReportLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.IntegerField(default=-1)),
                ('mission_id', models.IntegerField(default=-1)),
                ('module_name', models.CharField(default='', max_length=50)),
                ('local_path', models.TextField(default='')),
                ('local_ip', models.CharField(default='', max_length=50)),
                ('pid', models.CharField(default='', max_length=50)),
                ('run_time', models.CharField(default='', max_length=50)),
                ('check_time', models.CharField(default='', max_length=50)),
                ('monitor_link', models.TextField(default='')),
                ('script_res', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='SandboxReportVal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.IntegerField(default=-1)),
                ('item_name', models.CharField(default='', max_length=50)),
                ('item_val', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SandboxTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mission_id', models.IntegerField(default=-1)),
                ('module_name', models.CharField(default='', max_length=50)),
                ('is_master', models.IntegerField(default=-1)),
                ('have_update', models.IntegerField(default=-1)),
                ('need_check', models.IntegerField(default=-1)),
                ('run_time', models.CharField(default='', max_length=50)),
                ('check_time', models.CharField(default='', max_length=50)),
                ('is_checked', models.IntegerField(default=-1)),
                ('is_checked_ok', models.IntegerField(default=-1)),
                ('fail_reason', models.TextField(default='')),
                ('need_rollback', models.IntegerField(default=-1)),
                ('local_path', models.TextField(default='')),
                ('local_ip', models.CharField(default='', max_length=50)),
                ('pid', models.CharField(default='', max_length=50)),
                ('need_report', models.IntegerField(default=0)),
            ],
        ),
    ]