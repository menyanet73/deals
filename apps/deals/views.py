import csv

from django.contrib.postgres.aggregates import ArrayAgg
from django.core.cache import cache
from django.db import models, transaction
from django.db.models import Count, OuterRef, Subquery, Sum
from rest_framework import request, response, status
from rest_framework.views import APIView

from apps.deals.models import Customer, Deal, Gem
from apps.deals.serializers import (CSVSerializer, DealValidateSerializer,
                                    ResponseSerializer)
from conf.settings import CHECK_DUPLICATES


class DealViewSet(APIView):
    cache_key = 'deal_viewset_cache'

    def post(self, request: request.Request, *args, **kwargs):
        serializer = CSVSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data.get('deals')
        file_data = file.read().decode('utf-8')
        lines = file_data.split('\n')
        reader = csv.DictReader(lines, delimiter=',')

        with transaction.atomic():
            deals = []
            for row in reader:
                deal_serializer = DealValidateSerializer(data=row)
                deal_serializer.is_valid(raise_exception=True)

                customer, _ = Customer.objects.get_or_create(
                    username=deal_serializer.validated_data.pop('customer'))

                item, _ = Gem.objects.get_or_create(
                    name=deal_serializer.validated_data.pop('item'))

                if CHECK_DUPLICATES and Deal.objects.filter(
                    customer=customer,
                    item=item,
                    **deal_serializer.validated_data
                ).exists():
                    print('Deal already exists.')
                    continue

                deals.append(
                    Deal(
                        customer=customer,
                        item=item,
                        **deal_serializer.validated_data))

            Deal.objects.bulk_create(deals)
            if deals:
                cache.clear()

        return response.Response(
            data='Файл был обработан без ошибок',
            status=status.HTTP_200_OK)

    def get(self, request: request.Request, *args, **kwargs):
        cache_value = cache.get(key=self.cache_key, default=None)
        if cache_value:
            return response.Response(data=cache_value)

        top_customers = Customer.get_top_customers()

        gems_buyed_by_2_customers_from_top = Gem.get_gems_buyed_by_customers(
            customers=top_customers)

        top_customers = top_customers.annotate(
            gems=Subquery(
            Gem.objects.filter(
                name__in=gems_buyed_by_2_customers_from_top.values_list(
                    'name', flat=True)
            ).filter(
                deals__customer=OuterRef('id')
            ).values('deals__customer').annotate(
                gems=ArrayAgg('name', distinct=True)
            ).values('gems'),
            output_field=models.CharField(null=False),),)

        data = {'response': [customer for customer in top_customers]}
        response_serializer = ResponseSerializer(data=data)
        response_serializer.is_valid(raise_exception=True)

        cache.set(key=self.cache_key, value=response_serializer.data)

        return response.Response(data=response_serializer.data, status=status.HTTP_200_OK)
