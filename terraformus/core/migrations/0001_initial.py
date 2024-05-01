# Generated by Django 5.0.4 on 2024-05-01 20:19

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="LifeCycle",
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
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("bu", "Build"),
                            ("op", "Operation"),
                            ("en", "End of life"),
                        ],
                        default="Build",
                        max_length=2,
                    ),
                ),
                ("total_duration", models.TextField(help_text="help text placeholder")),
                ("description", models.TextField(help_text="help text placeholder")),
            ],
        ),
        migrations.CreateModel(
            name="LifeCycleInput",
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
                (
                    "resource_name",
                    models.CharField(help_text="help text placeholder", max_length=255),
                ),
                (
                    "resource_type",
                    models.CharField(
                        choices=[
                            ("hu", "Human"),
                            ("se", "Service"),
                            ("ma", "Material"),
                        ],
                        help_text="help text placeholder",
                        max_length=2,
                    ),
                ),
                (
                    "unit",
                    models.CharField(help_text="help text placeholder", max_length=255),
                ),
                ("quantity", models.IntegerField(help_text="help text placeholder")),
                (
                    "reference_cost",
                    models.IntegerField(help_text="help text placeholder"),
                ),
                (
                    "notes",
                    models.TextField(
                        blank=True, help_text="help text placeholder", null=True
                    ),
                ),
                (
                    "lifecycle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.lifecycle"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LifeCycleWaste",
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
                ("waste_type", models.TextField(help_text="help text placeholder")),
                (
                    "reusable",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "recyclable",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "cradle2cradle",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "unit",
                    models.CharField(help_text="help text placeholder", max_length=255),
                ),
                ("quantity", models.IntegerField(help_text="help text placeholder")),
                (
                    "reference_cost",
                    models.IntegerField(help_text="help text placeholder"),
                ),
                (
                    "destination_method",
                    models.TextField(help_text="help text placeholder"),
                ),
                (
                    "notes",
                    models.TextField(
                        blank=True, help_text="help text placeholder", null=True
                    ),
                ),
                (
                    "lifecycle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.lifecycle"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
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
                ("biography", models.TextField(blank=True, max_length=5000, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Solution",
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
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="An identifiable unique name for this solution.",
                        max_length=255,
                        unique=True,
                    ),
                ),
                (
                    "subtitle",
                    models.CharField(
                        help_text="A secondary explanation of what this solution is.",
                        max_length=255,
                    ),
                ),
                (
                    "goal",
                    models.TextField(
                        help_text="What problem your solution aims to solve"
                    ),
                ),
                (
                    "automation",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "infrastructure",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "extreme_poverty",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "lower_class",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "middle_class",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "upper_class",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "individual",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "apartment",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "house",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "apartment_building",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "street",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "house_complex",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "neighborhood",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "town",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "city",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "county",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "state",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "country",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "continent",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "planet",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "no_poverty",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "zero_hunger",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "good_health_and_well_being",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "quality_education",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "gender_equality",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "clean_water_and_sanitation",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "affordable_and_clean_energy",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "decent_work_and_economic_growth",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "industry_innovation_and_infrastructure",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "reduced_inequality",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "sustainable_cities_and_communities",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "responsible_consumption_and_production",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "climate_action",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "life_below_water",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "life_on_land",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "peace_justice_and_strong_institutions",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "partnerships_for_the_goals",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "housing",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "food",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "energy",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "water",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "health",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "communication",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "education",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "transportation",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "security",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "governance",
                    models.BooleanField(
                        default=False, help_text="help text placeholder"
                    ),
                ),
                (
                    "cost_type",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "0"),
                            (1, "$"),
                            (2, "$$"),
                            (3, "$$$"),
                            (4, "$$$$"),
                        ],
                        default="0",
                        help_text="help text placeholder",
                    ),
                ),
                ("update", models.TextField(help_text="help text placeholder")),
                ("upgrade", models.TextField(help_text="help text placeholder")),
                ("scale_up", models.TextField(help_text="help text placeholder")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("edited_at", models.DateTimeField(auto_now=True)),
                (
                    "depends_on",
                    models.ManyToManyField(
                        blank=True,
                        help_text="help text placeholder",
                        related_name="dependencies",
                        to="core.solution",
                    ),
                ),
                (
                    "derives_from",
                    models.ForeignKey(
                        blank=True,
                        help_text="help text placeholder",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="derived_solutions",
                        to="core.solution",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="lifecycle",
            name="solution",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.solution"
            ),
        ),
        migrations.CreateModel(
            name="Strategy",
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
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                (
                    "title",
                    models.CharField(help_text="help text placeholder", max_length=255),
                ),
                ("goal", models.TextField(help_text="help text placeholder")),
                (
                    "definitions",
                    models.TextField(
                        help_text="help text placeholder - includes limitations"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ExternalAsset",
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
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("we", "Working example"),
                            ("re", "Reference"),
                            ("do", "Document"),
                        ],
                        default="Document",
                        max_length=255,
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("url", models.URLField(help_text="help text placeholder")),
                (
                    "solution",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.solution",
                    ),
                ),
                (
                    "strategy",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.strategy",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StrategySolution",
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
                ("notes", models.TextField(help_text="help text placeholder")),
                (
                    "solution",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="core.solution"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="strategy",
            name="solutions",
            field=models.ManyToManyField(
                help_text="help text placeholder", to="core.strategysolution"
            ),
        ),
    ]
