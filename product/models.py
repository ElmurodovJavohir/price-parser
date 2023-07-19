from tabnanny import verbose
from unittest.mock import Base

from django.db import models
from django.utils.html import mark_safe

from utils.models import BaseModel


class Product(BaseModel):
    name = models.CharField(max_length=512, verbose_name="Название")
    price = models.CharField(max_length=512, verbose_name="Цена")

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
