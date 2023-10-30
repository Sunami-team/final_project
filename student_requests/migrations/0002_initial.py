# Generated by Django 4.2.6 on 2023-10-29 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student_requests', '0001_initial'),
        ('users', '0001_initial'),
        ('courses', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='termdroprequest',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student'),
        ),
        migrations.AddField(
            model_name='termdroprequest',
            name='term',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.term'),
        ),
        migrations.AddField(
            model_name='militaryservicerequest',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student'),
        ),
        migrations.AddField(
            model_name='militaryservicerequest',
            name='term',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.term'),
        ),
        migrations.AddField(
            model_name='gradereconsiderationrequest',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.courseterm'),
        ),
        migrations.AddField(
            model_name='gradereconsiderationrequest',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student'),
        ),
        migrations.AddField(
            model_name='emergencydroprequest',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.courseterm'),
        ),
        migrations.AddField(
            model_name='emergencydroprequest',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student'),
        ),
        migrations.AddField(
            model_name='courseregistrationrequest',
            name='requested_courses',
            field=models.ManyToManyField(to='courses.courseterm'),
        ),
        migrations.AddField(
            model_name='courseregistrationrequest',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student'),
        ),
        migrations.AddField(
            model_name='coursecorrectionrequest',
            name='courses_to_add',
            field=models.ManyToManyField(related_name='add_requests', to='courses.courseterm'),
        ),
        migrations.AddField(
            model_name='coursecorrectionrequest',
            name='courses_to_drop',
            field=models.ManyToManyField(related_name='drop_requests', to='courses.courseterm'),
        ),
        migrations.AddField(
            model_name='coursecorrectionrequest',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student'),
        ),
    ]