# Generated by Django 4.1.4 on 2023-01-09 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calender", "0002_reservation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reservation",
            name="age",
            field=models.CharField(
                blank=True,
                choices=[("u", "14세이상"), ("d", "14세미만")],
                max_length=1,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="email",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="grade",
            field=models.CharField(
                blank=True,
                choices=[("1", "1학년"), ("2", "2학년"), ("3", "3학년"), ("n", "기타")],
                max_length=1,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="headcount",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="motivation",
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="name",
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="phone",
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="school",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="status",
            field=models.CharField(
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
    ]
