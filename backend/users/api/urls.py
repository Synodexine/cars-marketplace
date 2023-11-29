from django.urls import path
from rest_framework.authtoken import views

from users.api.views import RegistrationView


urlpatterns = [
    path("obtain-token/", views.obtain_auth_token),
    path("register/", RegistrationView.as_view()),
]
