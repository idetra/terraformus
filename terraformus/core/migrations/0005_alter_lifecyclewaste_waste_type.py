# Generated by Django 5.0.4 on 2024-05-31 13:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_alter_lifecycle_title_alter_lifecycle_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lifecyclewaste",
            name="waste_type",
            field=models.CharField(help_text="help text placeholder", max_length=255),
        ),
    ]
