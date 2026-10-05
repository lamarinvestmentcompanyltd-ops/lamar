import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import InquiryForm
from .models import (
    Material,
    Partner,
    ServiceCategory,
    TeamMember,
    Testimonial,
    WorkPhoto,
    WorkPhotoCategory,
)

logger = logging.getLogger(__name__)


def home(request):
    partners = Partner.objects.all()
    testimonials = Testimonial.objects.all()
    return render(request, "core/home.html", {"partners": partners, "testimonials": testimonials})


def about(request):
    team = TeamMember.objects.all()
    return render(request, "core/about.html", {"team": team})


def services(request):
    return render(request, "core/services.html")


def why_choose_us(request):
    return render(request, "core/why_choose_us.html")


def health_safety(request):
    return render(request, "core/health_safety.html")


def privacy(request):
    return render(request, "core/privacy.html")


def faq(request):
    return render(request, "core/faq.html")


def robots_txt(request):
    sitemap_url = request.build_absolute_uri("/sitemap.xml")
    content = f"User-agent: *\nAllow: /\n\nSitemap: {sitemap_url}\n"
    return HttpResponse(content, content_type="text/plain")


def sitemap_xml(request):
    urls = [
        ("home", 1.0),
        ("about", 0.8),
        ("services", 0.8),
        ("why_choose_us", 0.6),
        ("health_safety", 0.6),
        ("gallery", 0.6),
        ("materials", 0.6),
        ("faq", 0.5),
        ("contact", 0.9),
        ("privacy", 0.3),
    ]
    entries = []
    for name, priority in urls:
        loc = request.build_absolute_uri(reverse(name))
        entries.append(f"  <url>\n    <loc>{loc}</loc>\n    <priority>{priority}</priority>\n  </url>")
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(entries)
        + "\n</urlset>"
    )
    return HttpResponse(xml, content_type="application/xml")


def _build_gallery_items():
    """Group WorkPhoto rows into before/after pairs (matched by pair_key)
    plus standalone items, in a single ordered list ready for the template."""
    photos = list(WorkPhoto.objects.all())
    used_ids = set()
    items = []

    paired_keys = {p.pair_key for p in photos if p.pair_key}
    for key in paired_keys:
        group = [p for p in photos if p.pair_key == key]
        before = next((p for p in group if p.category == WorkPhotoCategory.BEFORE), None)
        after = next((p for p in group if p.category == WorkPhotoCategory.AFTER), None)
        if before and after:
            items.append({"type": "pair", "before": before, "after": after, "order": min(before.order, after.order)})
            used_ids.update([before.pk, after.pk])

    for photo in photos:
        if photo.pk not in used_ids:
            items.append({"type": "single", "photo": photo, "order": photo.order})

    items.sort(key=lambda i: i["order"])
    return items


def gallery(request):
    items = _build_gallery_items()
    return render(request, "core/gallery.html", {"items": items})


def materials(request):
    """Our Materials — grouped by category so the template can render a
    section per group. Categories with no items are skipped automatically."""
    all_materials = list(Material.objects.all())
    groups = []
    for key, label in Material.CATEGORY_CHOICES:
        in_group = [m for m in all_materials if m.category == key]
        if in_group:
            groups.append({"key": key, "label": label, "items": in_group})
    return render(request, "core/materials.html", {"groups": groups})


def _notify_new_inquiry(inquiry):
    subject = f"New inquiry from {inquiry.name} — {inquiry.get_service_display()}"
    body = (
        f"Name: {inquiry.name}\n"
        f"Email: {inquiry.email}\n"
        f"Phone: {inquiry.phone or '—'}\n"
        f"Service: {inquiry.get_service_display()}\n\n"
        f"Message:\n{inquiry.message}\n\n"
        f"— View/manage this in the admin under Core > Inquiries."
    )
    try:
        # reply_to = the visitor, so hitting "Reply" in your inbox answers them directly.
        EmailMessage(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [settings.LAMAR_NOTIFY_EMAIL],
            reply_to=[inquiry.email],
        ).send(fail_silently=False)
    except Exception:
        # Never let an email failure break the visitor's form submission —
        # the inquiry is already saved in the database either way.
        logger.exception("Failed to send inquiry notification email for inquiry id=%s", inquiry.pk)


def contact(request):
    if request.method == "POST":
        form = InquiryForm(request.POST)
        if form.is_valid():
            if form.is_spam():
                # Pretend it worked — don't tip off bots that they were caught.
                messages.success(
                    request,
                    "Thanks — your request has been received. We'll get back to you shortly.",
                )
                return redirect("contact")
            inquiry = form.save()
            _notify_new_inquiry(inquiry)
            messages.success(
                request,
                "Thanks — your request has been received. We'll get back to you shortly.",
            )
            return redirect("contact")
    else:
        initial = {}
        requested_service = request.GET.get("service")
        if requested_service in ServiceCategory.values:
            initial["service"] = requested_service
        form = InquiryForm(initial=initial)
    return render(request, "core/contact.html", {"form": form})
