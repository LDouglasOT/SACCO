# Generated by Django 5.0.4 on 2024-05-06 09:21

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0008_alter_customuser_options_alter_customuser_managers_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="user",
        ),
        migrations.CreateModel(
            name="Users",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("firstname", models.CharField(max_length=255)),
                ("lastname", models.CharField(max_length=255)),
                ("location", models.CharField(max_length=255)),
                ("birthday", models.CharField(max_length=255)),
                ("phoneNumber", models.CharField(max_length=255, unique=True)),
                (
                    "profilepic",
                    models.ImageField(blank=True, null=True, upload_to="profile_pics/"),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, null=True, unique=True
                    ),
                ),
                ("password", models.CharField(max_length=255)),
                ("createdAt", models.DateTimeField(auto_now_add=True)),
                ("updatedAt", models.DateTimeField(auto_now=True)),
                (
                    "accountId",
                    models.CharField(
                        blank=True, max_length=255, null=True, unique=True
                    ),
                ),
                ("isAdmin", models.BooleanField(default=False)),
                ("isActive", models.BooleanField(default=False)),
                (
                    "membershipNumber",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("membershipType", models.CharField(max_length=255)),
                (
                    "HomeAddress",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("dateofbirth", models.DateTimeField()),
                ("nationality", models.CharField(max_length=255)),
                ("nationalId", models.CharField(max_length=255)),
                ("placeofwork", models.CharField(max_length=255)),
                ("natureofwork", models.CharField(max_length=255)),
                ("gender", models.CharField(max_length=255)),
                ("MaritalStatus", models.CharField(max_length=255)),
                ("nextofkin", models.CharField(max_length=255)),
                ("nextofkinphone", models.CharField(max_length=255)),
                ("nextofkinaddress", models.CharField(max_length=255)),
                (
                    "account",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="Account",
                        to="home.account",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="users",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="User",
        ),
    ]
