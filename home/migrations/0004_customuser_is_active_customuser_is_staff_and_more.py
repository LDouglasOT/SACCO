# Generated by Django 5.0.4 on 2024-05-06 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0003_customuser_alter_account_accountowner_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="is_staff",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="customuser",
            name="username",
            field=models.CharField(default="684a339f09", max_length=255, unique=True),
        ),
    ]
