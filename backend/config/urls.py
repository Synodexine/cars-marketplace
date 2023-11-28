from django.contrib import admin
from django.urls import path, include

from marketplace.api.urls import urlpatterns as marketplace_urls
from users.api.urls import urlpatterns as users_urls


api_urls = [
    path('', include(marketplace_urls), name='marketplace'),
    path('', include(users_urls), name='users')
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls), name='api'),
]
