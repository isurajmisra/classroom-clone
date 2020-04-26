# Generated by Django 3.0.2 on 2020-01-14 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answers',
            name='created_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='classroom',
            name='c_code',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='questions',
            name='created_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
