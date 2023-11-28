from django.contrib import admin
from django.urls import path, include

from marketplace.api.urls import urlpatterns as marketplace_urls


api_urls = [
    path('', include(marketplace_urls), name='marketplace')
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls), name='api'),
]
