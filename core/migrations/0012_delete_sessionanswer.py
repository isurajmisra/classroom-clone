# Generated by Django 3.0.2 on 2020-01-17 05:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_remove_joinedusersession_classroom'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SessionAnswer',
        ),
    ]