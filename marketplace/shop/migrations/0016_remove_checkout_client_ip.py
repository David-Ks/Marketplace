# Generated by Django 4.0.6 on 2022-08-09 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_alter_product_options_checkout_client_ip'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkout',
            name='client_ip',
        ),
    ]