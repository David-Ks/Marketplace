# Generated by Django 4.0.6 on 2022-07-16 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='for_view',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]