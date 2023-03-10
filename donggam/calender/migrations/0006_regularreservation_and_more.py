# Generated by Django 4.1.4 on 2023-01-11 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calender", "0005_delete_event"),
    ]

    operations = [
        migrations.CreateModel(
            name="RegularReservation",
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
                    "age",
                    models.CharField(
                        blank=True,
                        choices=[("u", "14세이상"), ("d", "14세미만")],
                        max_length=1,
                        null=True,
                    ),
                ),
                ("parent_name", models.CharField(blank=True, max_length=12, null=True)),
                (
                    "parent_phone",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                ("name", models.CharField(blank=True, max_length=12, null=True)),
                ("phone", models.CharField(blank=True, max_length=15, null=True)),
                ("email", models.CharField(blank=True, max_length=50, null=True)),
                ("school", models.CharField(blank=True, max_length=30, null=True)),
                (
                    "grade",
                    models.CharField(
                        blank=True,
                        choices=[("1", "1학년"), ("2", "2학년"), ("3", "3학년"), ("n", "기타")],
                        max_length=1,
                        null=True,
                    ),
                ),
                ("headcount", models.IntegerField(blank=True, null=True)),
                ("motivation", models.TextField(blank=True, max_length=200, null=True)),
                ("request", models.TextField(blank=True, max_length=200, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("0", "신청가능"),
                            ("1", "신청대기"),
                            ("2", "검토중"),
                            ("3", "승인완료"),
                            ("4", "신청마감"),
                        ],
                        max_length=1,
                    ),
                ),
            ],
        ),
        migrations.RenameField(
            model_name="reservation", old_name="motivation", new_name="memo",
        ),
        migrations.RemoveField(model_name="reservation", name="age",),
        migrations.RemoveField(model_name="reservation", name="request",),
        migrations.AddField(
            model_name="reservation",
            name="bus",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="reservation",
            name="length",
            field=models.IntegerField(
                blank=True, choices=[(6, "60분"), (9, "90분")], null=True
            ),
        ),
        migrations.AddField(
            model_name="reservation",
            name="major",
            field=models.IntegerField(
                blank=True, choices=[(0, "공통"), (1, "문과"), (2, "이과")], null=True
            ),
        ),
    ]
