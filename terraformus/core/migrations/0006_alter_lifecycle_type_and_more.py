# Generated by Django 5.0.4 on 2024-06-02 16:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_alter_lifecyclewaste_waste_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lifecycle",
            name="type",
            field=models.CharField(
                choices=[("b", "Build"), ("o", "Operation"), ("e", "End of life")],
                default="Build",
                help_text='Also known as "phase" of a life cycle',
                max_length=2,
            ),
        ),
        migrations.AlterField(
            model_name="lifecycleinput",
            name="resource_type",
            field=models.CharField(
                choices=[("ma", "Material"), ("se", "Service"), ("hu", "Human")],
                help_text="help text placeholder",
                max_length=2,
            ),
        ),
    ]
