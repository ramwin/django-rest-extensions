# Generated by Django 2.2.6 on 2019-11-20 06:32

from django.db import migrations
import rest_extensions.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='extra',
            field=rest_extensions.fields.ColorField(null=True),
        ),
    ]
