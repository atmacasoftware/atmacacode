from rest_framework.response import Response
from rest_framework.views import APIView
from adminpage.models import *
from adminpage.serializers import *

class BlogApiView(APIView):
    def get(self, request):
        try:
            blog = Blog.objects.select_related().filter(status='Yayınla')
            serializer = BlogSerializer(blog, many=True)
            return Response({'data': serializer.data})
        except Blog.DoesNotExist:
            return Response({'msg': 'Blog bulunmamaktadır.'})

    def post(self, request):
        return Response({'msg': 'Bu apide post methodu çalışmamaktadır.'})