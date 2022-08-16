# Generated by Django 4.1 on 2022-08-15 05:19

import courses.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Pricing",
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
                ("name", models.CharField(max_length=100)),
                ("slug", models.SlugField(unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name="chapter",
            name="video",
            field=models.FileField(
                default=1, upload_to=courses.models.user_directory_path
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="course",
            name="video",
            field=models.FileField(
                default=1, upload_to=courses.models.user_directory_path
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="lesson",
            name="video",
            field=models.FileField(
                default=1, upload_to=courses.models.user_directory_path
            ),
            preserve_default=False,
        ),
    ]
