from django.urls import path
from blog.views import blog_page, blog_details, category_details,search,blog_tags,submit_review

urlpatterns = [
    path("", blog_page, name="blog_pages"),
    path("<slug:slug>", blog_details, name="blog_details"),
    path("kategoriler/<slug:slug>", category_details, name="category_details"),
    path("kategoriler/anahtar-kelime/<str:keyword>", blog_tags, name="blog_tags"),
    path("yorum-ekle/<username>/<int:blog_id>", submit_review, name="submit_review"),
    path('blog/arama/', search, name='search'),
]
