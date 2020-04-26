# Generated by Django 3.0.2 on 2020-01-16 06:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_questions_classroom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='classroom',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='core.Classroom'),
        ),
    ]