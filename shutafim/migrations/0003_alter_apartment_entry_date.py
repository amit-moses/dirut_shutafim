# Generated by Django 4.2.3 on 2023-07-27 14:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shutafim', '0002_alter_apartment_entry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='entry_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
