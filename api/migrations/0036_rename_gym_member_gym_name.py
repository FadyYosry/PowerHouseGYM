# Generated by Django 4.1.7 on 2023-05-25 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0035_rename_gym_name_member_gym'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='gym',
            new_name='gym_name',
        ),
    ]