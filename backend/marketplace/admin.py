from django.contrib import admin

from marketplace.models import (
    Brand,
    CarModel,
    Generation,
    ParameterType,
    Parameter,
    Advertisement,
)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Generation)
class GenerationAdmin(admin.ModelAdmin):
    pass


@admin.register(ParameterType)
class ParameterTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    pass


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    pass
