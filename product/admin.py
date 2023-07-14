from baton.admin import (
    ChoicesDropdownFilter,
    MultipleChoiceListFilter,
    SimpleDropdownFilter,
)
from django.contrib import admin
from django.db import models
from django.db.models.functions import Coalesce
from django.http import HttpResponseRedirect
from django.urls import path
from import_export.admin import ImportExportMixin

from competitor.models import Competitor
from product.models import Brand, Category, Product
from product.resources import ProductResource
from utils.admin_pagination import AdminDynPaginationMixin
from utils.dynamic_column import DynamicColumn


class ProductMatchChoices(models.TextChoices):
    YES = "True", "Только соответствующий продукт"


class StatusListFilter(SimpleDropdownFilter):
    title = "Соответствующий продукт"
    parameter_name = "match"

    def lookups(self, request, model_admin):
        return ProductMatchChoices.choices

    def queryset(self, request, queryset):
        if self.value() is not None:
            search_term = self.value()
            return queryset.filter(competitor_products__isnull=False)


class ProductAdmin(AdminDynPaginationMixin, ImportExportMixin, admin.ModelAdmin):
    resource_classes = [ProductResource]
    list_filter = ("category", "brand", StatusListFilter)
    list_display = ("name", "category", "brand", "format_price")
    search_fields = ("name",)
    autocomplete_fields = ["competitor_products"]
    baton_cl_includes = [
        (
            "product/product_changelist.html",
            "above",
        ),
    ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("match/", self.set_match),
        ]
        return my_urls + urls

    def set_match(self, request):
        from competitor.tasks import match_products_task

        match_products_task.delay()
        self.message_user(request, "Успешно завершено")
        return HttpResponseRedirect("../")

    def get_queryset(self, request):
        queryset = super(ProductAdmin, self).get_queryset(request)
        competitors = Competitor.objects.filter(is_active=True)
        products_competitors = {}
        for competitor in competitors:
            products_competitors[f"competitor_{competitor.id}"] = Coalesce(
                models.Avg(
                    "competitor_products__price",
                    filter=models.Q(competitor_products__competitor__id=competitor.id),
                    output_field=models.IntegerField(),
                ),
                None,
                output_field=models.IntegerField(),
            )

        queryset = queryset.annotate(**products_competitors)
        return queryset

    def get_list_display(self, request):
        competitors = Competitor.objects.filter(is_active=True)
        list_display = list(self.list_display)
        for competitor in competitors:
            list_display.append(
                DynamicColumn(
                    f"competitor_{competitor.id}",
                    f'<img src = "{competitor.logo}" width = "30"/> {competitor.name}',
                )
            )

        return list_display


class CategoryAdmin(AdminDynPaginationMixin, admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class BrandAdmin(AdminDynPaginationMixin, admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
