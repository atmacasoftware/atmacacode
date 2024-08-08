from rest_framework import serializers
from ecommerce.models import *

class MarketPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketPlaces
        fields = '__all__'

class SupportedTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportedTypes
        fields = '__all__'