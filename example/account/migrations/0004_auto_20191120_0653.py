# Generated by Django 2.2.6 on 2019-11-20 06:53

from django.db import migrations
import rest_extensions.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20191120_0642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='fav_color',
            field=rest_extensions.fields.ColorField(default=rest_extensions.fields.Color.default),
        ),
    ]
