# Generated by Django 3.2.20 on 2023-08-13 17:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shutafim', '0016_alter_messages_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
