# Generated by Django 4.0.6 on 2022-09-08 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_remove_profile_follower_remove_profile_following_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='following',
            old_name='follower_id',
            new_name='follower',
        ),
        migrations.RenameField(
            model_name='following',
            old_name='following_id',
            new_name='following',
        ),
    ]