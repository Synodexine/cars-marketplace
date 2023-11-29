from django.contrib.auth.models import User
from rest_framework import serializers
from drf_extra_fields.fields import DateRangeField

from marketplace.models import (
    Brand,
    CarModel,
    Generation,
    Parameter,
    ParameterType,
    Advertisement,
)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            "id",
            "name",
        ]


class CarModelSerializer(serializers.ModelSerializer):
    brand_id = serializers.IntegerField(write_only=True, min_value=1)

    class Meta:
        model = CarModel
        fields = [
            "id",
            "name",
            "brand_id",
        ]


class CarModelDetailSerializer(CarModelSerializer):
    class Meta:
        model = CarModel
        fields = [
            "id",
            "name",
            "brand",
            "generations",
            "brand_id",
        ]
        read_only_fields = ["brand", "generations"]
        depth = 1


class ParameterTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParameterType
        fields = ["id", "name"]


class ParameterTypeDetailSerializer(ParameterTypeSerializer):
    class Meta:
        model = ParameterType
        fields = ["id", "name", "parameters"]
        read_only_fields = ["parameters"]
        depth = 1


class ParameterSerializer(serializers.ModelSerializer):
    type_id = serializers.IntegerField(write_only=True, min_value=1)

    class Meta:
        model = Parameter
        fields = ["id", "name", "type_id"]


class ParameterDetailSerializer(ParameterSerializer):
    class Meta:
        model = Parameter
        fields = ["id", "name", "type_id", "type"]
        read_only_fields = ["type"]
        depth = 1


class GenerationSerializer(serializers.ModelSerializer):
    car_model_id = serializers.IntegerField(write_only=True, min_value=1)
    year = DateRangeField()

    class Meta:
        model = Generation
        fields = ["id", "name", "car_model_id", "year", "allowed_parameters"]
        extra_kwargs = {"allowed_parameters": {"write_only": True}}


class GenerationDetailSerializer(GenerationSerializer):
    allowed_parameters_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1), write_only=True
    )

    class Meta:
        model = Generation
        fields = [
            "id",
            "name",
            "car_model",
            "car_model_id",
            "year",
            "allowed_parameters",
            "allowed_parameters_ids",
        ]
        depth = 2
        read_only_fields = ["car_model"]

    def update(self, instance, validated_data):
        allowed_parameters = validated_data.get("allowed_parameters_ids")
        if allowed_parameters:
            instance.allowed_parameters.set(allowed_parameters)
            instance.save()
        return super(GenerationDetailSerializer, self).update(instance, validated_data)


class AdvertisementOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]


class AdvertisementListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ["id", "name", "description", "price", "mileage", "generation_id"]


class AdvertisementSearchSerializer(serializers.Serializer):
    brand = serializers.IntegerField(min_value=1, required=True)
    car_model = serializers.IntegerField(min_value=1, required=False)
    generation = serializers.IntegerField(min_value=1, required=False)
    year = serializers.IntegerField(min_value=1970, required=False)
    price_from = serializers.FloatField(min_value=0, required=False)
    price_to = serializers.FloatField(min_value=0, required=False)
    parameters = serializers.ListField(
        child=serializers.IntegerField(min_value=1), required=False
    )


class AdvertisementDetailSerializer(serializers.ModelSerializer):
    owner = AdvertisementOwnerSerializer()

    class Meta:
        model = Advertisement
        fields = [
            "id",
            "name",
            "description",
            "price",
            "mileage",
            "generation",
            "parameters",
            "owner",
            "is_approved",
        ]
        depth = 3


class AdvertisementCreateSerializer(AdvertisementListSerializer):
    class Meta:
        model = Advertisement
        fields = [
            "id",
            "description",
            "price",
            "generation",
            "parameters",
            "owner",
            "is_approved",
        ]
        read_only_fields = ["is_approved"]

    def create(self, validated_data):
        # this code allows to add only parameters that are exist in a generation
        parameters_ids = [
            parameter.id for parameter in validated_data.pop("parameters")
        ]
        advertisement = super(AdvertisementCreateSerializer, self).create(
            validated_data
        )
        parameters = advertisement.generation.allowed_parameters.filter(
            id__in=parameters_ids
        )
        advertisement.parameters.set(parameters)
        advertisement.save()
        return advertisement
