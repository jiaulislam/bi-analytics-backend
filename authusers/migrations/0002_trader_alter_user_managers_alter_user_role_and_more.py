# Generated by Django 5.0.3 on 2024-04-07 10:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authusers", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Trader",
            fields=[
                (
                    "branch_code",
                    models.IntegerField(
                        db_column="branch_Code", primary_key=True, serialize=False
                    ),
                ),
                (
                    "branch_name",
                    models.CharField(db_column="branch_Name", max_length=255),
                ),
                ("trader_id", models.CharField(db_column="trader_id", max_length=255)),
                (
                    "trader_name",
                    models.CharField(db_column="trader_name", max_length=255),
                ),
            ],
            options={
                "db_table": "BI_trd_Dealer_info",
                "managed": False,
            },
        ),
        migrations.AlterModelManagers(
            name="user",
            managers=[],
        ),
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("ADMIN", "Admin"),
                    ("MANAGEMENT", "Management"),
                    ("BRANCH_MANAGER", "Branch Manager"),
                    ("REGIONAL_MANAGER", "Regional Manager"),
                    ("CLUSTER_MANAGER", "Cluster Manager"),
                ],
                default="REGIONAL_MANAGER",
                max_length=55,
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="branch_id",
            field=models.IntegerField(blank=True, null=True, verbose_name="Branch Id"),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="branch_name",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Branch Name"
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="profile_images/",
                verbose_name="Profile Pic",
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="profile",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="Role",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("codename", models.CharField(max_length=255, unique=True)),
                ("viewname", models.CharField(max_length=255)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_by_%(class)s_related",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="updated_by_%(class)s_related",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "bi_access_role_levels",
                "ordering": ["-created_at"],
            },
        ),
    ]