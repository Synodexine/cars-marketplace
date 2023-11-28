from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from drf_extra_fields.fields import DateRangeField

from marketplace.models import Brand, CarModel, Generation, Parameter, ParameterType, Advertisement


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            'id',
            'name',
        ]


class CarModelSerializer(serializers.ModelSerializer):
    brand_id = serializers.IntegerField(write_only=True, min_value=1)

    class Meta:
        model = CarModel
        fields = [
            'id',
            'name',
            'brand_id',
        ]


class CarModelDetailSerializer(CarModelSerializer):
    class Meta:
        model = CarModel
        fields = [
            'id',
            'name',
            'brand',
            'generations',
            'brand_id',
        ]
        read_only_fields = ['brand', 'generations']
        depth = 1


class ParameterTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParameterType
        fields = [
            'id',
            'name'
        ]


class ParameterTypeDetailSerializer(ParameterTypeSerializer):
    class Meta:
        model = ParameterType
        fields = [
            'id',
            'name',
            'parameters'
        ]
        read_only_fields = ['parameters']
        depth = 1


class ParameterSerializer(serializers.ModelSerializer):
    type_id = serializers.IntegerField(write_only=True, min_value=1)

    class Meta:
        model = Parameter
        fields = [
            'id',
            'name',
            'type_id'
        ]


class ParameterDetailSerializer(ParameterSerializer):
    class Meta:
        model = Parameter
        fields = [
            'id',
            'name',
            'type_id',
            'type'
        ]
        read_only_fields = ['type']
        depth = 1


class GenerationSerializer(serializers.ModelSerializer):
    car_model_id = serializers.IntegerField(write_only=True, min_value=1)
    year = DateRangeField()

    class Meta:
        model = Generation
        fields = [
            'id',
            'name',
            'car_model_id',
            'year',
            'allowed_parameters'
        ]
        extra_kwargs = {'allowed_parameters': {'write_only': True}}


class GenerationDetailSerializer(GenerationSerializer):
    allowed_parameters_ids = serializers.ListField(child=serializers.IntegerField(min_value=1), write_only=True)

    class Meta:
        model = Generation
        fields = [
            'id',
            'name',
            'car_model',
            'car_model_id',
            'year',
            'allowed_parameters',
            'allowed_parameters_ids',
        ]
        depth = 2
        read_only_fields = ['car_model']

    def update(self, instance, validated_data):
        allowed_parameters = validated_data.get('allowed_parameters_ids')
        if allowed_parameters:
            instance.allowed_parameters.set(allowed_parameters)
            instance.save()
        return super().update(instance, validated_data)


