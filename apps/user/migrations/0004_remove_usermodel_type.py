# Generated by Django 4.1 on 2023-04-15 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_usermodel_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermodel',
            name='type',
        ),
    ]
