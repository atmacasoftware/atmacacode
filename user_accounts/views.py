from django.contrib.auth import authenticate
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from user_accounts.models import User
from user_accounts.seriazliers import UserSerializer, RegisterSerializer, LoginSerializer


# Create your views here.

def user_count(request):
    user_count = User.objects.all().count()
    student_count = User.objects.filter(is_student=True).count()
    customer_count = User.objects.filter(is_customer=True).count()
    admin_count = User.objects.filter(is_superuser=True).count()

    data = {'user_count':user_count, 'student_count':student_count, 'customer_count':customer_count, 'admin_count':admin_count}

    return data

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = RegisterSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_serializer.data,
            }, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)