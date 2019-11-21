# Generated by Django 2.1.1 on 2019-11-20 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sandbox_report', '0007_auto_20191120_2034'),
    ]

    operations = [
        migrations.CreateModel(
            name='SandboxReportLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.IntegerField(default=-1)),
                ('mission_id', models.IntegerField(default=-1)),
                ('module_name', models.CharField(blank=True, max_length=50, null=True)),
                ('local_path', models.TextField(blank=True, null=True)),
                ('local_ip', models.CharField(blank=True, max_length=50, null=True)),
                ('pid', models.CharField(blank=True, max_length=50, null=True)),
                ('run_time', models.CharField(blank=True, max_length=50, null=True)),
                ('check_time', models.CharField(blank=True, max_length=50, null=True)),
                ('monitor_link', models.TextField(blank=True, null=True)),
                ('script_res', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SandboxReportVal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.IntegerField(default=-1)),
                ('item_name', models.CharField(blank=True, max_length=50, null=True)),
                ('item_val', models.CharField(blank=True, max_length=50, null=True)),
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
                ('need_report', models.IntegerField(default=-1)),
            ],
        ),
    ]