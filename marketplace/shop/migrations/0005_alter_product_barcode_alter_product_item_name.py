# Generated by Django 4.0.6 on 2022-07-24 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='barcode',
            field=models.PositiveBigIntegerField(default=1, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='item_name',
            field=models.CharField(max_length=300, null=True, verbose_name='product title'),
        ),
    ]