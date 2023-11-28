from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView

from users.api.serializers import RegistrationSerializer


class RegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
