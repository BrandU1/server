# Generated by Django 4.1.3 on 2022-12-05 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0025_productimage_alter_product_tags_delete_productimages_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('url', models.URLField()),
            ],
        ),
    ]
