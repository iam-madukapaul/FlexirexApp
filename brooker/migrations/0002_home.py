# Generated by Django 4.2.3 on 2023-08-19 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brooker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Home',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_rewards', models.CharField(max_length=50)),
                ('online_user', models.CharField(max_length=50)),
                ('total_investor', models.CharField(max_length=50)),
                ('total_withdraw', models.CharField(max_length=50)),
                ('total_transaction', models.CharField(max_length=50)),
            ],
        ),
    ]
