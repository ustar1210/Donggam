# Generated by Django 4.1.4 on 2023-01-09 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calender", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Reservation",
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
                ("date", models.DateField()),
                (
                    "time",
                    models.CharField(
                        choices=[("10", "10:00"), ("14", "14:00")], max_length=2
                    ),
                ),
                (
                    "age",
                    models.CharField(
                        choices=[("u", "14세이상"), ("d", "14세미만")], max_length=1
                    ),
                ),
                ("name", models.CharField(max_length=12)),
                ("email", models.CharField(max_length=50)),
                ("school", models.CharField(max_length=30)),
                (
                    "grade",
                    models.CharField(
                        choices=[("1", "1학년"), ("2", "2학년"), ("3", "3학년"), ("n", "기타")],
                        max_length=1,
                    ),
                ),
                ("headcount", models.IntegerField()),
                ("phone", models.CharField(max_length=11)),
                ("motivation", models.TextField(max_length=200)),
                ("request", models.TextField(blank=True, max_length=200, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("0", "신청대기"), ("1", "검토중"), ("2", "승인완료")],
                        max_length=1,
                    ),
                ),
            ],
        ),
    ]
