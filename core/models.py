from django.db import models


class ServiceCategory(models.TextChoices):
    COMMERCIAL = "commercial", "Commercial Cleaning"
    RESIDENTIAL = "residential", "Residential Cleaning"
    INSTITUTIONAL = "institutional", "Institutional Cleaning"
    SPECIALIZED = "specialized", "Specialized Cleaning"
    NOT_SURE = "not_sure", "Not sure yet"


class Inquiry(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    service = models.CharField(
        max_length=20, choices=ServiceCategory.choices, default=ServiceCategory.NOT_SURE
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    handled = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Inquiries"

    def __str__(self):
        return f"{self.name} — {self.get_service_display()} ({self.created_at:%Y-%m-%d})"


class Partner(models.Model):
    name = models.CharField(max_length=120)
    logo = models.ImageField(upload_to="partners/")
    website = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first.")

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120, blank=True)
    photo = models.ImageField(upload_to="team/")
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first.")

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    client_name = models.CharField(max_length=120)
    client_detail = models.CharField(
        max_length=150, blank=True, help_text="e.g. company name, or 'Homeowner, Kicukiro'"
    )
    photo = models.ImageField(
        upload_to="testimonials/", blank=True, null=True,
        help_text="Optional. A photo of the client, or their company logo — shown next to the quote if provided.",
    )
    quote = models.TextField()
    rating = models.PositiveSmallIntegerField(
        default=5, help_text="1–5 stars. Leave at 5 if you don't want to bother tracking this."
    )
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first.")

    class Meta:
        ordering = ["order", "-id"]

    def __str__(self):
        return f"{self.client_name} ({self.rating}★)"


class Material(models.Model):
    """Products, equipment and supplies Lamar uses on the job — shown on the
    public 'Our Materials' page. Manageable entirely from /admin/."""

    CATEGORY_CHOICES = [
        ("equipment", "Equipment & Machines"),
        ("chemicals", "Cleaning Products & Chemicals"),
        ("consumables", "Consumables & Supplies"),
        ("safety", "Safety & Protective Gear"),
    ]

    name = models.CharField(max_length=140)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="equipment"
    )
    description = models.TextField(
        blank=True,
        help_text="Optional. A short line on what it's used for.",
    )
    image = models.ImageField(
        upload_to="materials/",
        blank=True,
        null=True,
        help_text="Optional. A photo of the product or equipment.",
    )
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first.")

    class Meta:
        ordering = ["category", "order", "name"]

    def __str__(self):
        return self.name


class WorkPhotoCategory(models.TextChoices):
    BEFORE = "before", "Before"
    AFTER = "after", "After"
    GENERAL = "general", "General work"


class WorkPhoto(models.Model):
    image = models.ImageField(upload_to="work/")
    caption = models.CharField(max_length=150, blank=True)
    category = models.CharField(
        max_length=10, choices=WorkPhotoCategory.choices, default=WorkPhotoCategory.GENERAL
    )
    pair_key = models.CharField(
        max_length=60,
        blank=True,
        help_text=(
            "Optional. Give a 'before' and an 'after' photo the same pair_key "
            "(e.g. 'office-oct-2026') to link them as a before/after set."
        ),
    )
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first.")

    class Meta:
        ordering = ["order", "-id"]

    def __str__(self):
        return self.caption or f"Work photo #{self.pk}"
