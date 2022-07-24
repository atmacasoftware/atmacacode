from django.shortcuts import render

# Create your views here.

from django.views.generic import TemplateView
# Create your views here.

class RobotsTxtView(TemplateView):
    template_name = "robots.txt"
    content_type = "text/plain"