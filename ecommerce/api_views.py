from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ecommerce.serializers import *
from ecommerce.models import *

@api_view(['GET'])
def marketplace_api(request):
    try:
        marketplaces = MarketPlaces.objects.filter(is_active=True)
        serializer = MarketPlaceSerializer(marketplaces, many=True)
        data = serializer.data
        return Response({'data': data}, status=status.HTTP_200_OK)
    except Exception as e:
        data = str(e)
        return Response({'data': data}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def supported_type_api(request):
    try:
        supported_type = SupportedTypes.objects.all()
        serializer = SupportedTypesSerializer(supported_type, many=True)
        data = serializer.data
        return Response({'data': data}, status=status.HTTP_200_OK)
    except Exception as e:
        data = str(e)
        return Response({'data': data}, status=status.HTTP_400_BAD_REQUEST)

