# Generated by Django 4.2.3 on 2023-08-02 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shutafim', '0006_rename_url_imagedata_myurl'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='kosher',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='title',
            field=models.CharField(default='', max_length=24),
        ),
    ]
