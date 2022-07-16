from django.urls import path
from blog.views import blog_page,blog_details,submit_review

urlpatterns = [
    path("",blog_page, name="blog_pages"),
    path("<slug:slug>",blog_details, name="blog_details"),
    path("yorum-ekle/<username>/<int:blog_id>",submit_review, name="submit_review"),
]