from rest_framework import serializers
from apps.deals.models import Customer, Gem

from apps.deals.validators import validate_csv_file


class CSVSerializer(serializers.Serializer):
    deals = serializers.FileField(validators=[validate_csv_file,])


class DealValidateSerializer(serializers.Serializer):
    customer = serializers.CharField()
    item = serializers.CharField()
    total = serializers.FloatField()
    quantity = serializers.IntegerField()
    date = serializers.DateTimeField()


class CustomerSerializer(serializers.Serializer):
    username = serializers.SlugRelatedField(
        slug_field='username', queryset=Customer.objects.all())
    spent_money = serializers.FloatField()
    gems = serializers.ListField(
        child=serializers.SlugRelatedField(
            slug_field='name', queryset=Gem.objects.all()))


class ResponseSerializer(serializers.Serializer):
    response = CustomerSerializer(many=True)
