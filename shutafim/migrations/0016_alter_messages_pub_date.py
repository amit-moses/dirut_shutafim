# Generated by Django 3.2.20 on 2023-08-13 17:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shutafim', '0015_rename_datetime_messages_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='pub_date',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]