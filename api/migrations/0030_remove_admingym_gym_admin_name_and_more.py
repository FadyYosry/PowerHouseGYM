# Generated by Django 4.1.7 on 2023-03-11 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_admingym_delete_admin_gym'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admingym',
            name='gym_admin_name',
        ),
        migrations.RemoveField(
            model_name='admingym',
            name='gym_name',
        ),
        migrations.RemoveField(
            model_name='gym',
            name='admin',
        ),
        migrations.AddField(
            model_name='admin',
            name='first_name',
            field=models.CharField(default='NULL', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='admin',
            name='last_name',
            field=models.CharField(default='NULL', max_length=100),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='AdminMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.gym')),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.admin')),
            ],
        ),
    ]
