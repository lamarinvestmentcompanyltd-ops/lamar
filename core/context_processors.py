from django.conf import settings


def analytics(request):
    """Makes GOOGLE_ANALYTICS_ID available in every template as
    `google_analytics_id`, without needing to pass it from every view."""
    return {"google_analytics_id": settings.GOOGLE_ANALYTICS_ID}
