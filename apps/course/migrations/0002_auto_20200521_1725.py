# Generated by Django 2.2.5 on 2020-05-21 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='video_url',
            field=models.URLField(blank=True),
        ),
    ]