# Generated by Django 4.0.6 on 2022-08-23 05:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0002_post_backdrop_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='backdrop_image',
        ),
    ]
