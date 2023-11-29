from django.urls import path
from rest_framework.routers import DefaultRouter

from marketplace.api.views import (
    BrandViewSet,
    CarModelListCreateView,
    CarModelRetrieveUpdateDestroyView,
    GenerationRetrieveUpdateDestroyView,
    GenerationListCreateView,
    ParameterTypeListCreateView,
    ParameterTypeRetrieveUpdateDestroyView,
    ParameterListCreateView,
    ParameterRetrieveUpdateDestroyView,
    ApproveAdvertisement,
    AdvertisementCreateView,
    AdvertisementListView,
    AdvertisementRetrieveDestroyView,
)


router = DefaultRouter()
router.register(r"brands", BrandViewSet, basename="brands")

urlpatterns = [
    path("models/", CarModelListCreateView.as_view()),
    path("models/<int:pk>/", CarModelRetrieveUpdateDestroyView.as_view()),
    path("generations/", GenerationListCreateView.as_view()),
    path("generations/<int:pk>/", GenerationRetrieveUpdateDestroyView.as_view()),
    path("parameter-types/", ParameterTypeListCreateView.as_view()),
    path("parameter-types/<int:pk>/", ParameterTypeRetrieveUpdateDestroyView.as_view()),
    path("parameters/", ParameterListCreateView.as_view()),
    path("parameters/<int:pk>/", ParameterRetrieveUpdateDestroyView.as_view()),
    path("advertisements/create/", AdvertisementCreateView.as_view()),
    path("advertisements/", AdvertisementListView.as_view()),
    path("advertisements/<int:pk>/", AdvertisementRetrieveDestroyView.as_view()),
    path("advertisements/<int:pk>/approve/", ApproveAdvertisement.as_view()),
] + router.urls
