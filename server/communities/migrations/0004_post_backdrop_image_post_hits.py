# Generated by Django 4.0.6 on 2022-08-24 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0003_remove_post_backdrop_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='backdrop_image',
            field=models.ImageField(null=True, upload_to='community/backdrop/%Y-%m'),
        ),
        migrations.AddField(
            model_name='post',
            name='hits',
            field=models.PositiveIntegerField(default=1),
        ),
    ]