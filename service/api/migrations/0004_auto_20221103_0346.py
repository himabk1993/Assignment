# Generated by Django 3.2.16 on 2022-11-03 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_auto_20221102_1854"),
    ]

    operations = [
        migrations.RenameField(
            model_name="apartment",
            old_name="deleted_by",
            new_name="user_id",
        ),
        migrations.RenameField(
            model_name="building",
            old_name="deleted_by",
            new_name="user_id",
        ),
        migrations.RenameField(
            model_name="rentalagreement",
            old_name="deleted_by",
            new_name="user_id",
        ),
        migrations.AlterField(
            model_name="building",
            name="id",
            field=models.CharField(max_length=40, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="rentalagreement",
            name="id",
            field=models.CharField(max_length=40, primary_key=True, serialize=False),
        ),
    ]