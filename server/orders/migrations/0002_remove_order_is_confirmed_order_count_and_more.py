# Generated by Django 4.0.6 on 2022-09-14 07:46

from django.db import migrations, models
import orders.models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='is_confirmed',
        ),
        migrations.AddField(
            model_name='order',
            name='count',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(default=orders.models.generate_order_number, max_length=20, unique=True),
        ),
    ]
