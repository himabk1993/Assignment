# Generated by Django 3.2.16 on 2022-11-03 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_auto_20221103_0346"),
    ]

    operations = [
        migrations.RenameField(
            model_name="apartment",
            old_name="user_id",
            new_name="user",
        ),
        migrations.RenameField(
            model_name="building",
            old_name="user_id",
            new_name="user",
        ),
        migrations.RenameField(
            model_name="rentalagreement",
            old_name="user_id",
            new_name="user",
        ),
    ]
