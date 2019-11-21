# Generated by Django 2.1.1 on 2019-11-21 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sandbox_report', '0008_sandboxreportlink_sandboxreportval_sandboxtask'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sandboxtask',
            name='is_checked',
        ),
        migrations.AddField(
            model_name='sandboxreportlink',
            name='need_mail',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='sandboxtask',
            name='proc_top_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]