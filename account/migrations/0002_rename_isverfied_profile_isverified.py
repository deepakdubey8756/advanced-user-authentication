# Generated by Django 4.1.7 on 2023-04-01 03:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='isVerfied',
            new_name='isVerified',
        ),
    ]