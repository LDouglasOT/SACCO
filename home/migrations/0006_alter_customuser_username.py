# Generated by Django 5.0.4 on 2024-05-06 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_customuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(default='804097c797', max_length=255, unique=True),
        ),
    ]
