# Generated by Django 4.2.2 on 2023-09-17 17:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0008_email"),
    ]

    operations = [
        migrations.CreateModel(
            name="FormSubmission",
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
                ("uuid", models.UUIDField(unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name="email",
            name="task",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="watchers",
                to="tasks.task",
            ),
        ),
    ]
