# Generated by Django 4.0.6 on 2022-07-25 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_item_checkout'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='is_paied',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
