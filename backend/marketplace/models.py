from django.db import models
from django.contrib.postgres.fields import DateRangeField


class Brand(models.Model):
    name = models.CharField(max_length=256, unique=True)


class CarModel(models.Model):
    name = models.CharField(max_length=256)
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='car_models'
    )


class Generation(models.Model):
    name = models.CharField(max_length=256)
    car_model = models.ForeignKey(
        CarModel,
        on_delete=models.CASCADE,
        related_name='generations'
    )
    year = DateRangeField()
    allowed_parameters = models.ManyToManyField('Parameter', related_name='generations')


class ParameterType(models.Model):
    name = models.CharField(max_length=256, unique=True)


class Parameter(models.Model):
    name = models.CharField(max_length=256, unique=True)
    type = models.ForeignKey(
        ParameterType,
        on_delete=models.CASCADE,
        related_name='parameters'
    )


class Advertisement(models.Model):
    description = models.CharField(max_length=512)
    price = models.FloatField(default=0)
    generation = models.ForeignKey(
        Generation,
        on_delete=models.CASCADE,
        related_name='advertisements'
    )
    parameters = models.ManyToManyField(Parameter)



