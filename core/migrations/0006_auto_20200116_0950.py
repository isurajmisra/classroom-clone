# Generated by Django 3.0.2 on 2020-01-16 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200116_0801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='multiplechoiceanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mcq_a', to='core.Questions'),
        ),
    ]