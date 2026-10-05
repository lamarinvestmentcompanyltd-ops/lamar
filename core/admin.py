import csv

from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html

from .models import Inquiry, Material, Partner, TeamMember, Testimonial, WorkPhoto


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "service", "created_at", "handled")
    list_filter = ("service", "handled", "created_at")
    search_fields = ("name", "email", "phone", "message")
    readonly_fields = ("created_at",)
    actions = ["export_as_csv"]

    @admin.action(description="Export selected inquiries as CSV")
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="inquiries.csv"'
        writer = csv.writer(response)
        writer.writerow(["Name", "Email", "Phone", "Service", "Message", "Submitted", "Handled"])
        for inquiry in queryset.order_by("-created_at"):
            writer.writerow([
                inquiry.name,
                inquiry.email,
                inquiry.phone,
                inquiry.get_service_display(),
                inquiry.message,
                inquiry.created_at.strftime("%Y-%m-%d %H:%M"),
                "Yes" if inquiry.handled else "No",
            ])
        return response


def _thumb(image_field, size=40):
    if not image_field:
        return "—"
    return format_html(
        '<img src="{}" style="height:{}px;width:{}px;object-fit:cover;border-radius:4px;" />',
        image_field.url, size, size,
    )


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("logo_preview", "name", "website", "order")
    list_editable = ("order",)
    ordering = ("order", "name")
    fields = ("name", "logo", "website", "order")

    @admin.display(description="Logo")
    def logo_preview(self, obj):
        return _thumb(obj.logo)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("photo_preview", "name", "role", "order")
    list_editable = ("order",)
    ordering = ("order", "name")
    fields = ("name", "role", "photo", "order")

    @admin.display(description="Photo")
    def photo_preview(self, obj):
        return _thumb(obj.photo)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("photo_preview", "client_name", "client_detail", "rating", "order")
    list_editable = ("order",)
    ordering = ("order", "-id")
    fields = ("client_name", "client_detail", "photo", "quote", "rating", "order")

    @admin.display(description="Photo")
    def photo_preview(self, obj):
        return _thumb(obj.photo)


@admin.register(WorkPhoto)
class WorkPhotoAdmin(admin.ModelAdmin):
    list_display = ("image_preview", "caption", "category", "pair_key", "order")
    list_filter = ("category",)
    list_editable = ("order",)
    ordering = ("order", "-id")
    fields = ("image", "caption", "category", "pair_key", "order")

    @admin.display(description="Image")
    def image_preview(self, obj):
        return _thumb(obj.image, size=50)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("image_preview", "name", "category", "order")
    list_filter = ("category",)
    list_editable = ("order",)
    ordering = ("category", "order", "name")
    search_fields = ("name", "description")
    fields = ("name", "category", "description", "image", "order")

    @admin.display(description="Image")
    def image_preview(self, obj):
        return _thumb(obj.image, size=50)


# --- Custom dashboard stats on the admin homepage ---
# Wraps the built-in admin index view to inject a few "at a glance" counts,
# rendered by the custom templates/admin/index.html (project-level template,
# takes priority over jazzmin's default via TEMPLATES DIRS).
_original_admin_index = admin.site.index


def _dashboard_index(request, extra_context=None):
    extra_context = extra_context or {}
    extra_context["lamar_stats"] = {
        "new_inquiries": Inquiry.objects.filter(handled=False).count(),
        "total_inquiries": Inquiry.objects.count(),
        "team_members": TeamMember.objects.count(),
        "partners": Partner.objects.count(),
        "testimonials": Testimonial.objects.count(),
        "gallery_photos": WorkPhoto.objects.count(),
        "materials": Material.objects.count(),
    }
    return _original_admin_index(request, extra_context=extra_context)


admin.site.index = _dashboard_index
