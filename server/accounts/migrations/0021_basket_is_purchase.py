# Generated by Django 4.0.6 on 2022-09-19 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_alter_following_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='is_purchase',
            field=models.BooleanField(default=False),
        ),
    ]
