# Generated by Django 4.2.3 on 2023-07-27 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_account_is_deposit_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='is_deposit_active',
        ),
    ]
