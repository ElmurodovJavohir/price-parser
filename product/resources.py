from django.db import models
from django.db.models.functions import Coalesce
from import_export import fields, resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from competitor.models import Competitor
from product.models import Brand, Category, Product


class DynamicColumn:
    def __init__(self, column_name, name):
        self.column_name = column_name
        self.__name__ = ""
        self.short_description = name

    def __call__(self, widget) -> str:
        number = getattr(widget, self.column_name, "-")
        if str(number).isnumeric():
            return "{:,}".format(int(number)).replace(",", " ")
        return number


class ProductResource(resources.ModelResource):
    category = fields.Field(
        column_name="category",
        attribute="category",
        widget=ForeignKeyWidget(Category, field="name"),
    )
    brand = fields.Field(
        column_name="brand", attribute="brand", widget=ForeignKeyWidget(Brand, field="name")
    )

    def before_import_row(self, row, **kwargs):
        category_name = row["category"]
        Category.objects.get_or_create(name=category_name, defaults={"name": category_name})

        brand_name = row["brand"]
        Brand.objects.get_or_create(name=brand_name, defaults={"name": brand_name})

    class Meta:
        model = Product
        fields = ("name", "category", "brand", "price")
        import_id_fields = ("name",)

    def __init__(self):
        super().__init__()

        competitors = Competitor.objects.filter(is_active=True)
        for competitor in competitors:
            self.fields[f"competitor_{competitor.id}"] = Field(
                attribute=f"competitor_{competitor.id}",
                column_name=competitor.name,
                readonly=True,
            )

    def get_queryset(self):
        # queryset = super().get_queryset(request)
        queryset = Product.objects.all()
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
