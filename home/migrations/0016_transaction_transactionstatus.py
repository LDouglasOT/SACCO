# Generated by Django 5.0.4 on 2024-05-21 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0015_transaction_transactiondescription"),
    ]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="transactionStatus",
            field=models.CharField(default="pending", max_length=255),
        ),
    ]