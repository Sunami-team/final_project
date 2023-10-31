<<<<<<< HEAD
# Generated by Django 4.2.6 on 2023-10-29 18:39
=======
# Generated by Django 4.2.6 on 2023-10-29 20:01
>>>>>>> b541cb0eb1ab4b6c4bd351bdc3cfaa5dfa7d43d3

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CourseCorrectionRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approval_status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CourseRegistrationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approval_status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='EmergencyDropRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.BooleanField(default=False)),
                ('student_comment', models.TextField()),
                ('deputy_educational_comment', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GradeReconsiderationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reconsideration_text', models.TextField()),
                ('response_text', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MilitaryServiceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proof_document', models.FileField(upload_to='military_docs/')),
                ('issuance_place', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TermDropRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(choices=[('With Seniority', 'With Seniority'), ('Without Seniority', 'Without Seniority')], max_length=50)),
                ('student_comment', models.TextField()),
                ('deputy_educational_comment', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
