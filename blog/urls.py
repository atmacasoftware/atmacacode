from django.urls import path
from blog.views import blog_page,blog_details

urlpatterns = [
    path("",blog_page, name="blog_pages"),
    path("<slug:slug>/",blog_details, name="blog_details"),
]