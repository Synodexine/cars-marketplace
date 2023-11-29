from datetime import date

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db.models.expressions import Q
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView,
                                     RetrieveDestroyAPIView)

from marketplace.api.serializers import (BrandSerializer, CarModelSerializer, CarModelDetailSerializer,
                                         GenerationSerializer, GenerationDetailSerializer, ParameterTypeSerializer,
                                         ParameterTypeDetailSerializer, ParameterSerializer, ParameterDetailSerializer,
                                         AdvertisementListSerializer, AdvertisementCreateSerializer,
                                         AdvertisementDetailSerializer, AdvertisementSearchSerializer)
from marketplace.models import Brand, CarModel, Generation, ParameterType, Parameter, Advertisement
from marketplace.services.advertisement import approve_advertisement
from marketplace.permissions import IsAdminOrReadOnly


class BrandViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()


class CarModelListCreateView(ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CarModelSerializer
    queryset = CarModel.objects.all()
    filterset_fields = ['brand_id']


class CarModelRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CarModelDetailSerializer
    queryset = CarModel.objects.all()


class GenerationListCreateView(ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = GenerationSerializer
    queryset = Generation.objects.all()
    filterset_fields = ['car_model_id']


class GenerationRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = GenerationDetailSerializer
    queryset = Generation.objects.all()


class ParameterTypeListCreateView(ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ParameterTypeSerializer
    queryset = ParameterType.objects.all()


class ParameterTypeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ParameterTypeDetailSerializer
    queryset = ParameterType.objects.all()


class ParameterListCreateView(ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ParameterSerializer
    queryset = Parameter.objects.all()


class ParameterRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ParameterDetailSerializer
    queryset = Parameter.objects.all()


class AdvertisementCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = AdvertisementCreateSerializer
    queryset = Advertisement.objects.all()

    def create(self, request, *args, **kwargs):
        request.data['owner'] = request.user.id
        return super(AdvertisementCreateView, self).create(request, *args, **kwargs)


class ApproveAdvertisement(CreateAPIView):
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        try:
            advertisement = Advertisement.objects.get(pk=kwargs.get('pk'))
        except ObjectDoesNotExist as e:
            return Response({'detail': e.args})
        return Response({'success': approve_advertisement(request.user, advertisement)})


class AdvertisementListView(ListAPIView):
    serializer_class = AdvertisementListSerializer

    def get_queryset(self):
        serializer = AdvertisementSearchSerializer(data=self.request.query_params)
        if serializer.is_valid(raise_exception=True):
            # applying filters by query parameters if they were passed
            q = Q()
            q &= Q(generation__car_model__brand_id=serializer.data.get('brand'))
            if not self.request.user.is_staff:
                q &= Q(is_approved=True)
            if 'car_model' in serializer.data:
                q &= Q(generation__car_model_id=serializer.data.get('car_model'))
            if 'generation' in serializer.data:
                q &= Q(generation__id=serializer.data.get('generation'))
            if 'year' in serializer.data:
                year = serializer.data.get('year')
                q &= Q(generation__year__startswith__lte=date(year, 1, 1))
                q &= Q(generation__year__endswith__gte=date(year, 1, 1))
            if 'price_from' in serializer.data:
                price_from = serializer.data.get('price_from')
                q &= Q(price__gte=price_from)
            if 'price_to' in serializer.data:
                price_to = serializer.data.get('price_to')
                q &= Q(price__lte=price_to)
            if 'parameters' in serializer.data:
                parameters = serializer.data.get('parameters')
                q &= Q(parameters__in=parameters)
            filtered_ads = Advertisement.objects.filter(q)
            return filtered_ads


class AdvertisementRetrieveDestroyView(RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = AdvertisementDetailSerializer
    queryset = Advertisement.objects.all()

    def get(self, request, *args, **kwargs):
        # makes unapproved advertisements visible only for admins and owners
        if request.user.is_staff or self.queryset.filter(id=self.kwargs['pk'], owner=request.user):
            return super(AdvertisementRetrieveDestroyView, self).get(request, *args, **kwargs)
        raise PermissionDenied()

    def destroy(self, request, *args, **kwargs):
        # makes unapproved advertisements destroyable only for admins and owners
        if request.user.is_staff or self.queryset.filter(id=self.kwargs['pk'], owner=request.user):
            return super(AdvertisementRetrieveDestroyView, self).destroy(request, *args, **kwargs)
        raise PermissionDenied()

