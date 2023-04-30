from django.contrib import admin
from django.urls import path

from apps.deals.views import DealViewSet
from conf.yasg import urlpatterns as docs_urls

urlpatterns = [
    path('api/v1/deals/', DealViewSet.as_view(), name='deals'),
    path('admin/', admin.site.urls),
]

urlpatterns += docs_urls
