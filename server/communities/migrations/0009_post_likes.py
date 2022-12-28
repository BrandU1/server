# Generated by Django 4.1.3 on 2022-12-27 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_rename_basket_profile_baskets_and_more'),
        ('communities', '0008_postimage_rename_tag_posttag_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='post_likes', to='accounts.profile'),
        ),
    ]