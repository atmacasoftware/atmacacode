from django.contrib.sitemaps import Sitemap

from blog.models import Blog
from products.models import *

class BlogMap(Sitemap):
    def items(self):
        return Blog.objects.all()

class ProductMap(Sitemap):
    def items(self):
        return Services.objects.all()
