# Generated by Django 4.1.7 on 2023-03-09 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_admin_gym_gym_admin_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gym',
            name='admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gym', to='api.admin'),
        ),
    ]
