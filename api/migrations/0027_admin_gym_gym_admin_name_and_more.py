# Generated by Django 4.1.7 on 2023-03-09 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_admin_gym_gym_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin_gym',
            name='gym_admin_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='admin_gym',
            name='gym_admin_username',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]