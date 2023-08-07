from django.db import models
from utils.models import BaseModel
# Create your models here.


class AutoBrand(BaseModel):
    title = models.CharField(max_length=50)


class AutoModel(BaseModel):
    title = models.CharField(max_length=50)
    brand = models.ForeignKey(AutoBrand, on_delete=models.CASCADE)


class AutoPosition(BaseModel):
    title = models.CharField(max_length=50)
    model = models.ForeignKey(AutoModel, on_delete=models.CASCADE)


class AutoCity(BaseModel):
    title = models.CharField(max_length=50)


class Auto(BaseModel):
    autoelon_id = models.IntegerField(unique=True)
    brand = models.ForeignKey(
        AutoBrand, related_name="auto", on_delete=models.CASCADE)
    model = models.ForeignKey(
        AutoModel, related_name="auto", on_delete=models.CASCADE)
    position = models.ForeignKey(
        AutoPosition, related_name="auto", on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(
        AutoCity, related_name="auto", on_delete=models.CASCADE)

    price = models.IntegerField()
    year = models.SmallIntegerField()
    engine_capacity = models.FloatField()
    engine_fuel = models.CharField(max_length=50)
    body_type = models.CharField(max_length=50)
    transmission = models.CharField(max_length=50)
    drive_unit = models.CharField(max_length=50)

    description = models.TextField(null=True, blank=True)
