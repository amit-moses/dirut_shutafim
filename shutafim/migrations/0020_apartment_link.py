# Generated by Django 3.2.20 on 2023-08-16 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shutafim', '0019_alter_messages_mes_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='link',
            field=models.CharField(default=None, max_length=150, null=True),
        ),
    ]
