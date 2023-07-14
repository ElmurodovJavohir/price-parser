from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from competitor.models import (
    Competitor,
    CompetitorProduct,
    CompetitorSetting,
    CompetitorUrls,
    ProductPriceHistory,
)
from utils.admin_pagination import AdminDynPaginationMixin


class CompetitorProductAdmin(AdminDynPaginationMixin, admin.ModelAdmin):
    list_filter = ("competitor",)
    search_fields = ("name",)


class CompetitorAdmin(AdminDynPaginationMixin, admin.ModelAdmin, DynamicArrayMixin):
    list_display = ("logo_preview", "name", "url", "is_active")
    readonly_fields = ("logo_preview",)
    list_editable = ("is_active",)
    search_fields = ("url",)
    list_display_links = ("name",)
    baton_cl_includes = [
        (
            "competitor/competitor_changelist.html",
            "above",
        ),
    ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("parse/", self.set_match),
        ]
        return my_urls + urls

    def set_match(self, request):
        from competitor.tasks import parse_start

        parse_start.delay()
        self.message_user(request, "Успешно начать")
        return HttpResponseRedirect("../")


class CompetitorSettingAdmin(AdminDynPaginationMixin, admin.ModelAdmin, DynamicArrayMixin):
    pass


class ProductPriceHistoryAdmin(admin.ModelAdmin):
    autocomplete_fields = ["product"]


class CompetitorUrlsAdmin(AdminDynPaginationMixin, admin.ModelAdmin):
    list_display = ("url", "type", "competitor")
    list_filter = ("type", "competitor")
    search_fields = ("url",)


admin.site.register(Competitor, CompetitorAdmin)
admin.site.register(CompetitorUrls, CompetitorUrlsAdmin)
admin.site.register(CompetitorSetting, CompetitorSettingAdmin)
admin.site.register(CompetitorProduct, CompetitorProductAdmin)
admin.site.register(ProductPriceHistory, ProductPriceHistoryAdmin)
