from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("why-choose-us/", views.why_choose_us, name="why_choose_us"),
    path("health-safety/", views.health_safety, name="health_safety"),
    path("gallery/", views.gallery, name="gallery"),
    path("materials/", views.materials, name="materials"),
    path("faq/", views.faq, name="faq"),
    path("privacy/", views.privacy, name="privacy"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path("sitemap.xml", views.sitemap_xml, name="sitemap_xml"),
    path("contact/", views.contact, name="contact"),
]
