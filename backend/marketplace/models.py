from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import DateRangeField


class Brand(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return f'{self.name} [{self.id}]'


class CarModel(models.Model):
    name = models.CharField(max_length=256)
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='car_models'
    )

    def __str__(self):
        return f'{self.name} [{self.id}]'


class Generation(models.Model):
    name = models.CharField(max_length=256)
    car_model = models.ForeignKey(
        CarModel,
        on_delete=models.CASCADE,
        related_name='generations'
    )
    year = DateRangeField()
    allowed_parameters = models.ManyToManyField('Parameter', related_name='generations')

    def __str__(self):
        year = f'{self.year.lower.year}-{self.year.upper.year}'
        return f'{self.car_model.brand.name} {self.car_model.name} {self.name}, {year}'


class ParameterType(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return f'{self.name} [{self.id}]'


class Parameter(models.Model):
    name = models.CharField(max_length=256)
    type = models.ForeignKey(
        ParameterType,
        on_delete=models.CASCADE,
        related_name='parameters'
    )

    def __str__(self):
        return f'{self.name} [{self.id}]'


class Advertisement(models.Model):
    description = models.CharField(max_length=512)
    price = models.FloatField(default=0)
    mileage = models.IntegerField(default=0)
    generation = models.ForeignKey(
        Generation,
        on_delete=models.CASCADE,
        related_name='advertisements'
    )
    parameters = models.ManyToManyField(Parameter)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='advertisements',
        default=None
    )
    is_approved = models.BooleanField(default=False)

    @property
    def name(self):
        return str(self.generation)

    def __str__(self):
        return f'{self.name} [{self.id}]'
