# Generated by Django 4.1 on 2023-01-24 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calender", "0017_alter_reservation_status"),
    ]

    operations = [
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
                    ("5", "휴일"),
                    ("6", "거부"),
                    ("7", "재검토"),
                ],
                max_length=1,
            ),
        ),
    ]
