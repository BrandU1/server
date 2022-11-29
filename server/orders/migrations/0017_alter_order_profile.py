# Generated by Django 4.0.6 on 2022-11-23 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_profile_backdrop_image_alter_profile_profile_image'),
        ('orders', '0016_alter_delivery_invoice_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='accounts.profile'),
        ),
    ]
