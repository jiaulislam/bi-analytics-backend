# Generated by Django 5.0.3 on 2024-04-08 10:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authusers", "0002_trader_alter_user_managers_alter_user_role_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="role",
            name="codename",
            field=models.CharField(
                max_length=255, unique=True, verbose_name="Code Name"
            ),
        ),
        migrations.AlterField(
            model_name="role",
            name="viewname",
            field=models.CharField(max_length=255, verbose_name="View Name"),
        ),
    ]
