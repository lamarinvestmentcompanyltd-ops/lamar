from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_testimonial_photo"),
    ]

    operations = [
        migrations.CreateModel(
            name="Material",
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
                ("name", models.CharField(max_length=140)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("equipment", "Equipment & Machines"),
                            ("chemicals", "Cleaning Products & Chemicals"),
                            ("consumables", "Consumables & Supplies"),
                            ("safety", "Safety & Protective Gear"),
                        ],
                        default="equipment",
                        max_length=20,
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Optional. A short line on what it's used for.",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="Optional. A photo of the product or equipment.",
                        null=True,
                        upload_to="materials/",
                    ),
                ),
                (
                    "order",
                    models.PositiveIntegerField(
                        default=0, help_text="Lower numbers show first."
                    ),
                ),
            ],
            options={
                "ordering": ["category", "order", "name"],
            },
        ),
    ]
