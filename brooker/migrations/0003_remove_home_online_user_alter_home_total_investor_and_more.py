# Generated by Django 4.2.3 on 2023-08-19 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brooker', '0002_home'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='home',
            name='online_user',
        ),
        migrations.AlterField(
            model_name='home',
            name='total_investor',
            field=models.CharField(max_length=9),
        ),
        migrations.AlterField(
            model_name='home',
            name='total_rewards',
            field=models.CharField(max_length=9),
        ),
        migrations.AlterField(
            model_name='home',
            name='total_transaction',
            field=models.CharField(max_length=9),
        ),
        migrations.AlterField(
            model_name='home',
            name='total_withdraw',
            field=models.CharField(max_length=9),
        ),
    ]
