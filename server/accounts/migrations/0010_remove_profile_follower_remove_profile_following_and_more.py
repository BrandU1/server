# Generated by Django 4.0.6 on 2022-08-12 08:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_notify'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='follower',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='following',
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(upload_to='profile/%Y/%m/%d'),
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='accounts.profile')),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='accounts.profile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
