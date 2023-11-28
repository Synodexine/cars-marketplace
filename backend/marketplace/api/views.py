from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from marketplace.api.serializers import (BrandSerializer, CarModelSerializer, CarModelDetailSerializer,
                                         GenerationSerializer, GenerationDetailSerializer, ParameterTypeSerializer,
                                         ParameterTypeDetailSerializer, ParameterSerializer, ParameterDetailSerializer)
from marketplace.models import Brand, CarModel, Generation, ParameterType, Parameter


class BrandViewSet(ModelViewSet):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()


class CarModelListCreateView(ListCreateAPIView):
    serializer_class = CarModelSerializer
    queryset = CarModel.objects.all()
    filterset_fields = ['brand_id']


class CarModelRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = CarModelDetailSerializer
    queryset = CarModel.objects.all()


class GenerationListCreateView(ListCreateAPIView):
    serializer_class = GenerationSerializer
    queryset = Generation.objects.all()
    filterset_fields = ['car_model_id']


class GenerationRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = GenerationDetailSerializer
    queryset = Generation.objects.all()


class ParameterTypeListCreateView(ListCreateAPIView):
    serializer_class = ParameterTypeSerializer
    queryset = ParameterType.objects.all()


class ParameterTypeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ParameterTypeDetailSerializer
    queryset = ParameterType.objects.all()


class ParameterListCreateView(ListCreateAPIView):
    serializer_class = ParameterSerializer
    queryset = Parameter.objects.all()


class ParameterRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ParameterDetailSerializer
    queryset = Parameter.objects.all()
