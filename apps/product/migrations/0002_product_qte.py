# Generated by Django 4.1 on 2023-04-23 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='qte',
            field=models.ImageField(default=10, upload_to=''),
        ),
    ]
