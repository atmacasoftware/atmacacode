from django.contrib.sitemaps import Sitemap

from products.models import *

class ProductMap(Sitemap):
    def items(self):
        return Services.objects.all()
