# Generated by Django 4.1.6 on 2023-02-20 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DailyNet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("daily_date", models.DateField()),
                ("daily_net_earnings", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="DailyPaid",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("paid_date", models.DateField()),
                ("paid_amount", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="DailySpent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("spent_date", models.DateField()),
                ("spent_amount", models.FloatField()),
                ("spent_name", models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name="Debt",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("debt_name", models.CharField(max_length=64)),
                ("debt_type", models.CharField(max_length=64)),
                ("debt_amount", models.FloatField()),
            ],
        ),
    ]
