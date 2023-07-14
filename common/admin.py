# admin.site.register(Category)
# admin.site.register(Book)
# admin.site.register(Grocery)
from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.db import models
from django.template.response import TemplateResponse
from django_celery_beat.admin import *

from competitor.models import Competitor


def index(self, request, extra_context=None):
    """
    Display the main admin index page, which lists all of the installed
    apps that have been registered in this site.
    """

    competitors = (
        Competitor.objects.all()
        .annotate(products_count=models.Count("products"))
        .order_by("name")
        .values_list("name", "products_count")
    )
    context = {
        **self.each_context(request),
        "title": self.index_title,
        "subtitle": None,
        "competitors_label": ",".join([competitor[0] for competitor in competitors]),
        "competitors_data": [competitor[1] for competitor in competitors],
        **(extra_context or {}),
    }
    request.current_app = self.name

    return TemplateResponse(request, "baton/index.html", context)


AdminSite.index = index
# from .models import Book, Category, Grocery

# Register your models here.

# models = apps.get_models()

# for model in models:
#     try:
#         admin.site.register(model)
#     except admin.sites.AlreadyRegistered:
#         pass
