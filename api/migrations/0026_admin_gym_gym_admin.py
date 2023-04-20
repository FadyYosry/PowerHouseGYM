# Generated by Django 4.1.7 on 2023-03-09 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_remove_admin_created_at_remove_admin_updated_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin_gym',
            name='gym_admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gym_admin', to='api.admin'),
        ),
    ]