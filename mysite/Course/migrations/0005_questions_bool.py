# Generated by Django 5.1.4 on 2024-12-12 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0004_alter_lessonvideo_video_coursematerial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='bool',
            field=models.BooleanField(default=False),
        ),
    ]
