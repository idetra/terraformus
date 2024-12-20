# Generated by Django 5.0.4 on 2024-05-31 12:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_alter_externalasset_title_alter_externalasset_type_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lifecycle",
            name="title",
            field=models.CharField(help_text="help text placeholder", max_length=255),
        ),
        migrations.AlterField(
            model_name="lifecycle",
            name="type",
            field=models.CharField(
                choices=[("b", "Build"), ("o", "Operation"), ("e", "End of life")],
                default="Build",
                help_text="help text placeholder",
                max_length=2,
            ),
        ),
    ]
