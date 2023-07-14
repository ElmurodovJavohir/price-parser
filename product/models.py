from tabnanny import verbose
from unittest.mock import Base

from django.db import models
from django.utils.html import mark_safe

from competitor.models import Competitor, CompetitorProduct
from utils.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=256, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Brand(BaseModel):
    name = models.CharField(max_length=256, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"


class Product(BaseModel):
    name = models.CharField(max_length=512, verbose_name="Название")
    price = models.CharField(max_length=512, verbose_name="Цена")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name="Бренд")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    competitor_products = models.ManyToManyField(
        CompetitorProduct, related_name="main_product", blank=True
    )

    def format_price(self):
        return "{:,}".format(int(self.price)).replace(",", " ")

    format_price.short_description = mark_safe(
        "<img src='https://texnomart.uz/favicon.ico' width='30'> Цена"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
