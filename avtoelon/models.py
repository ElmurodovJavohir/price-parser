from django.db import models
from utils.models import BaseModel

# Create your models here.


class AutoLink(BaseModel):
    link = models.CharField(max_length=512, unique=True)
    is_parsed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.link


class AutoBrand(BaseModel):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.title


class AutoModel(BaseModel):
    title = models.CharField(max_length=50, unique=True)
    brand = models.ForeignKey(AutoBrand, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title


class AutoPosition(BaseModel):
    title = models.CharField(max_length=50)
    model = models.ForeignKey(AutoModel, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title


class AutoCity(BaseModel):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.title


class Auto(BaseModel):
    link = models.ForeignKey(AutoLink, related_name="auto", on_delete=models.CASCADE)

    # autoelon_id = models.IntegerField(unique=True)
    brand = models.ForeignKey(AutoBrand, related_name="auto", on_delete=models.CASCADE)
    model = models.ForeignKey(AutoModel, related_name="auto", on_delete=models.CASCADE)
    position = models.ForeignKey(
        AutoPosition, related_name="auto", on_delete=models.CASCADE, null=True, blank=True
    )
    city = models.ForeignKey(AutoCity, related_name="auto", on_delete=models.CASCADE)

    price = models.IntegerField()
    year = models.SmallIntegerField()
    engine_capacity = models.CharField(max_length=50, null=True, blank=True)
    engine_fuel = models.CharField(max_length=50, null=True, blank=True)
    body_type = models.CharField(max_length=50, null=True, blank=True)
    transmission = models.CharField(max_length=50, null=True, blank=True)
    drive_unit = models.CharField(max_length=50, null=True, blank=True)

    description = models.TextField(null=True, blank=True)

    @classmethod
    def create_or_update_auto(cls, auto_dict: dict, link):
        # BRAND
        brand, _ = AutoBrand.objects.get_or_create(title=auto_dict["brand"])
        # MODEL
        model, _ = AutoModel.objects.get_or_create(title=auto_dict["model"], brand=brand)
        # POSITION
        position = None
        if auto_dict["position"]:
            position, _ = AutoPosition.objects.get_or_create(
                title=auto_dict["position"], model=model
            )
        # CITY
        city, _ = AutoCity.objects.get_or_create(title=auto_dict["city"])

        # AUTO
        cls.objects.update_or_create(
            autoelon_id=auto_dict["autoelon_id"],
            link=link,
            defaults={
                "brand": brand,
                "model": model,
                "position": position,
                "city": city,
                "price": auto_dict["price"],
                "year": auto_dict["year"],
                "engine_capacity": auto_dict["engine_capacity"],
                "engine_fuel": auto_dict["engine_fuel"],
                "body_type": auto_dict["body_type"],
                "transmission": auto_dict["transmission"],
                "drive_unit": auto_dict["drive_unit"],
                "description": auto_dict["description"],
            },
        )
    