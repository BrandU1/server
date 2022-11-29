# Generated by Django 4.0.6 on 2022-08-12 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0001_initial'),
        ('accounts', '0012_follow_unique_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='scrapped',
            field=models.ManyToManyField(related_name='+', to='communities.post'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='accounts.profile'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='following',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followings', to='accounts.profile'),
        ),
    ]
