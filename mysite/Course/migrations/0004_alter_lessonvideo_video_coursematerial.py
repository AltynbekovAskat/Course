# Generated by Django 5.1.4 on 2024-12-11 11:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0003_course_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonvideo',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='lesson_video/'),
        ),
        migrations.CreateModel(
            name='CourseMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_material', models.FileField(upload_to='material/')),
                ('description', models.TextField()),
                ('courses', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='Course.course')),
            ],
        ),
    ]
