# Generated by Django 4.0.6 on 2022-07-28 03:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('accounts', '0004_address_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='memo',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='bucket',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='products.product'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bucket',
            field=models.ManyToManyField(related_name='+', through='accounts.Bucket', to='products.product'),
        ),
    ]
