# Generated by Django 3.0.2 on 2020-01-17 05:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0012_delete_sessionanswer'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionAnswers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=300)),
                ('class_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ClassroomSession')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='s_ans', to='core.Questions')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='s_ans', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]