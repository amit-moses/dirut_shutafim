# Generated by Django 4.2.3 on 2023-08-02 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shutafim', '0007_apartment_kosher_alter_apartment_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='agree_mail',
            field=models.BooleanField(default=True),
        ),
    ]
