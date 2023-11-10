# Generated by Django 4.2.6 on 2023-11-09 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('student', 'Student'), ('professor', 'Professor'), ('it_manager', 'IT Manager'), ('deputy_educational', 'Deputy Educational')], default='student', max_length=20),
        ),
    ]