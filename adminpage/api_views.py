from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from adminpage.models import *
from adminpage.serializers import *


class BlogApiView(APIView):
    def get(self, request):

        category = self.request.query_params.get('kategori')
        blogs = Blog.objects.select_related().filter(status='Yayınla').order_by('-created_at')

        if category:
            blogs = blogs.filter(category__slug=category)

        paginator = Paginator(blogs, 10)
        page = self.request.query_params.get('page')

        try:
            blog = paginator.page(page)
        except PageNotAnInteger:
            blog = paginator.page(1)
        except EmptyPage:
            blog = paginator.page(paginator.num_pages)

        serializer = BlogSerializer(blog, many=True)
        return Response({'data': serializer.data})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})


@api_view(['GET', "POST"])
def blog_detail(request, slug):
    data = None

    if request.method == 'POST':
        ip = request.META['REMOTE_ADDR']
        blog = get_object_or_404(Blog, slug=slug)

        if ip != '' or ip is not None:
            isIp = BlogUserIp.objects.filter(blog=blog, ip=ip).exists()
            if not isIp:
                BlogUserIp.objects.create(blog=blog, ip=ip)
                blog.view_count += 1
                blog.save()
    try:
        blog = get_object_or_404(Blog, slug=slug)
        serializer = BlogSerializer(blog, many=False)
        data = serializer.data
    except:
        data = "Bir hata meydana geldi."

    return Response({'data': data})


class BlogCategoryApiView(APIView):
    def get(self, request):
        try:
            category = BlogCategory.objects.select_related().all()
            serializer = BlogCategorySerializer(category, many=True)
            return Response({'data': serializer.data})
        except Blog.DoesNotExist:
            return Response({'msg': 'Blog bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})
