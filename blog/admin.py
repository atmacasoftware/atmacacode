from django.contrib import admin
from blog.models import Blog,ReviewRating
# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    list_display = ('user','category','title','is_main_choice','is_other_choice','blog_views','is_avalabile')
    search_fields = ('user','category','title')
    prepopulated_fields = {'slug':('title',)}
    list_per_page = 300

admin.site.register(Blog,BlogAdmin)
admin.site.register(ReviewRating)