from rest_framework import serializers
from adminpage.models import *

class BlogSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    user = serializers.CharField(source='user.get_full_name')
    user_photo = serializers.ImageField(source='user.image')
    user_bio = serializers.CharField(source='user.bio')
    user_github = serializers.CharField(source='user.github')
    user_linkedin = serializers.CharField(source='user.linkedin')
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    created_at = serializers.DateTimeField(read_only=True, format="%d-%m-%Y")
    updated_at = serializers.DateTimeField(read_only=True, format="%d-%m-%Y")

    class Meta:
        model = Blog
        fields = '__all__'

class BlogCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogCategory
        fields = '__all__'