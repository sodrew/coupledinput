# Generated by Django 3.2.22 on 2023-11-25 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CoupledInputUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(db_index=True, max_length=50)),
                ('student_id', models.CharField(db_index=True, max_length=32)),
                ('student_name', models.TextField(blank=True, default='')),
                ('name_one', models.TextField(blank=True, default='')),
                ('name_two', models.TextField(blank=True, default='')),
            ],
            options={
                'unique_together': {('course_id', 'student_id')},
            },
        ),
        migrations.CreateModel(
            name='CoupledInputResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(db_index=True, max_length=50)),
                ('student_id', models.CharField(db_index=True, max_length=32)),
                ('block_id', models.CharField(db_index=True, max_length=50)),
                ('prompt', models.TextField(blank=True, default='')),
                ('response_one', models.TextField(blank=True, default='')),
                ('response_two', models.TextField(blank=True, default='')),
            ],
            options={
                'unique_together': {('course_id', 'student_id', 'block_id')},
            },
        ),
    ]