# Generated by Django 4.0.6 on 2022-07-23 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_product_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
