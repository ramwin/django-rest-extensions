# Generated by Django 2.2.6 on 2019-11-20 06:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_extra'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='extra',
            new_name='fav_color',
        ),
    ]
