from django.urls import path
from adminpage.views import *
from ecommerce.api_views import *
from ecommerce.views import *

urlpatterns = [
    path('yonetim-paneli/entegrasyon-yonetimi/musteriler/', customers, name="ecommerce_customer"),
    path('yonetim-paneli/entegrasyon-yonetimi/abonelik-tipleri/', subscription, name="ecommerce_subscription"),
    path('yonetim-paneli/entegrasyon-yonetimi/pazaryerleri/', marketplace, name="ecommerce_marketplace"),
    path('yonetim-paneli/entegrasyon-yonetimi/desteklenen-xml/', supported_type, name="ecommerce_supported_type"),


    #### API ####
    path("api/v1/marketplaces/", marketplace_api, name="marketplace_api"),
    path("api/v1/supported-types/", supported_type_api, name="supported_type_api"),
]
