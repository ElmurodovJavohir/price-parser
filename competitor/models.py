import pgtrigger
from django.db import models
from django.utils.html import mark_safe
from django_better_admin_arrayfield.models.fields import ArrayField

from utils.models import BaseModel


class Competitor(models.Model):
    name = models.CharField(max_length=256)
    url = models.CharField(max_length=256, verbose_name="URL-адрес")

    logo = models.CharField(max_length=512, blank=True, null=True)

    is_active = models.BooleanField(default=True, verbose_name="Активный мониторинг")

    def __str__(self) -> str:
        return self.name

    def save(self):
        import requests

        image_formats = ("image/png", "image/jpeg", "image/jpg")
        try:
            res = requests.head(f"{self.url}/favicon.ico")
            if res.status_code == 200 and res.headers["content-type"] in image_formats:
                self.logo = res.url
        except:
            pass
        super().save()

    def logo_preview(self):  # new
        return mark_safe(f'<img src = "{self.logo}" width = "30"/>')

    logo_preview.short_description = "Логотип"
    logo_preview.allow_tags = True

    class Meta:
        ordering = ["-id"]
        verbose_name = "Конкурент"
        verbose_name_plural = "Конкуренты"


class CompetitorSetting(models.Model):
    competitor = models.OneToOneField(
        Competitor, on_delete=models.CASCADE, related_name="setting", verbose_name="Конкурент"
    )

    # SCRAPPING DETAILS
    sitemaps_urls = ArrayField(
        models.CharField(max_length=256, null=True, blank=True),
        null=True,
        blank=True,
        verbose_name="URL-адреса Sitemap",
    )

    page_pagination_slug = models.CharField(max_length=256, null=True, blank=True)

    category_slug = ArrayField(
        models.CharField(max_length=256, null=True, blank=True),
        null=True,
        blank=True,
    )
    product_slug = ArrayField(
        models.CharField(max_length=256, null=True, blank=True),
        null=True,
        blank=True,
    )

    category_parse = models.TextField()
    product_parse = models.TextField()

    def __str__(self) -> str:
        return f"{self.competitor} настройки"

    class Meta:
        verbose_name = "Настройка конкурентов"
        verbose_name_plural = "Настройки конкурентов"


CATEGORY_URL = "category"
PRODUCT_URL = "product"
URLS_CHOICES = (
    (CATEGORY_URL, "Category url"),
    (PRODUCT_URL, "Product url"),
)


class CompetitorUrls(models.Model):
    competitor = models.ForeignKey(
        Competitor,
        related_name="urls",
        on_delete=models.CASCADE,
        verbose_name="URL-адреса Sitemap",
    )
    type = models.CharField(max_length=25, choices=URLS_CHOICES, verbose_name="Тип")
    url = models.CharField(max_length=512, unique=True, verbose_name="URL-адрес")

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = "URL конкурентов"
        verbose_name_plural = "URL конкурентов"


class ProductPriceHistory(models.Model):
    product = models.ForeignKey(
        "CompetitorProduct", related_name="prices", on_delete=models.CASCADE, verbose_name="Продукт"
    )
    price = models.IntegerField(default=0, verbose_name="Цена")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = "История цен на товары"
        verbose_name_plural = "История цен на товары"


# Create your models here.
class CompetitorProduct(BaseModel):
    competitor = models.ForeignKey(
        Competitor,
        related_name="products",
        on_delete=models.CASCADE,
        verbose_name="Конкурент",
        db_index=True,
    )

    url = models.URLField(max_length=512, unique=True, verbose_name="URL-адрес")
    name = models.CharField(max_length=512, null=True, blank=True, verbose_name="Название")
    image = models.URLField(max_length=512, null=True, blank=True, verbose_name="Изображение")
    price = models.IntegerField(default=0, verbose_name="Цена")

    is_available = models.BooleanField(default=True, verbose_name="Доступен")

    class Meta:
        unique_together = ["competitor", "name"]
        verbose_name = "Продукт конкурента"
        verbose_name_plural = "Продукты конкурентов"
        triggers = [
            pgtrigger.Trigger(
                name="track_price_product_update",
                level=pgtrigger.Statement,
                when=pgtrigger.After,
                operation=pgtrigger.Update,
                referencing=pgtrigger.Referencing(new="new_values"),
                func=f"""
                    INSERT INTO {ProductPriceHistory._meta.db_table}(product_id, price,created_at)
                    SELECT
                        new_values.id AS product_id,
                        new_values.price AS price,
                        NOW()
                    FROM new_values;            
                    RETURN NULL;""",
            ),
            pgtrigger.Trigger(
                name="track_price_product_insert",
                level=pgtrigger.Statement,
                when=pgtrigger.After,
                operation=pgtrigger.Insert,
                referencing=pgtrigger.Referencing(new="new_values"),
                func=f"""
                    INSERT INTO {ProductPriceHistory._meta.db_table}(product_id, price,created_at)
                    SELECT
                        new_values.id AS product_id,
                        new_values.price AS price,
                        NOW()
                    FROM new_values;            
                    RETURN NULL;""",
            ),
        ]

    def __str__(self):
        return f"{self.name} -> {self.competitor.name}"
