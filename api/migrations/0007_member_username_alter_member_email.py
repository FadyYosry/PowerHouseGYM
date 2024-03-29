# Generated by Django 4.1.7 on 2023-02-16 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_gym_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='username',
            field=models.CharField(default='Unknown', max_length=50, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='member',
            name='email',
            field=models.EmailField(default='Unknown', max_length=254, unique=True),
            preserve_default=False,
        ),
    ]
