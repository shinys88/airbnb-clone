# Generated by Django 2.2.5 on 2021-07-01 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210701_0529'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='shorthost',
            new_name='superhost',
        ),
    ]
