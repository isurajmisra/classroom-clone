# Generated by Django 3.0.2 on 2020-01-16 12:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0006_auto_20200116_0950'),
    ]

    operations = [
        migrations.CreateModel(
            name='classroom_session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('answers_mcq', models.ManyToManyField(related_name='cs_mca', to='core.MultipleChoiceAnswer')),
                ('answers_short', models.ManyToManyField(related_name='cs_as', to='core.Answers')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class_sessions', to='core.Classroom')),
                ('questions', models.ManyToManyField(related_name='csq', to='core.Questions')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class_sessions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
