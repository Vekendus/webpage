"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from config.views import frontend_app
from gallery.views import (
    about_content,
    other_page_content,
    portfolio_gallery,
    service_list,
    slideshow_photo_list,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/slideshow/", slideshow_photo_list, name="slideshow-photo-list"),
    path("api/portfolio/", portfolio_gallery, name="portfolio-gallery"),
    path("api/about/", about_content, name="about-content"),
    path("api/services/", service_list, name="service-list"),
    path("api/pages/", other_page_content, name="other-page-content"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$",
            serve,
            {"document_root": settings.MEDIA_ROOT},
        ),
    ]

urlpatterns += [
    re_path(
        r"^(?!admin/|api/|media/|static/).*",
        frontend_app,
        name="frontend-app",
    ),
]
