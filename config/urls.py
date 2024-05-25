"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

from baton.autodiscover import admin
from django.conf import settings
from django.conf.urls.static import static

# from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from avtoelon.views import AutoDocumentView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
books = router.register(r"auto", AutoDocumentView, basename="auto")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("baton/", include("baton.urls")),
    # openapi
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/", include(router.urls)),
    path("", RedirectView.as_view(url="admin", permanent=False), name="index"),
]
# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
