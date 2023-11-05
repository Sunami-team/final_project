# Generated by Django 4.2 on 2023-11-01 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_initial'),
        ('student_requests', '0003_correctiontemporaryrequests'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='correctiontemporaryrequests',
            name='add_course',
        ),
        migrations.RemoveField(
            model_name='correctiontemporaryrequests',
            name='remove_course',
        ),
        migrations.AddField(
            model_name='correctiontemporaryrequests',
            name='add_or_remove',
            field=models.CharField(blank=True, choices=[('add', 'add'), ('remove', 'remove')], max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='correctiontemporaryrequests',
            name='select_course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='add_correction_courses', to='courses.courseterm'),
        ),
    ]