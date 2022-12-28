# Generated by Django 4.1.3 on 2022-12-27 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0007_remove_contentimage_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='community/%Y-%m')),
            ],
        ),
        migrations.RenameModel(
            old_name='Tag',
            new_name='PostTag',
        ),
        migrations.RemoveField(
            model_name='contentimage',
            name='content',
        ),
        migrations.RemoveField(
            model_name='review',
            name='profile',
        ),
        migrations.AddField(
            model_name='post',
            name='content',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='posts', to='communities.posttag'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=50),
        ),
        migrations.DeleteModel(
            name='Content',
        ),
        migrations.DeleteModel(
            name='ContentImage',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
        migrations.AddField(
            model_name='postimage',
            name='content',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='communities.post'),
        ),
    ]
