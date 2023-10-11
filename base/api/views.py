from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer, FileSerializer
from base.models import File

from django.views.decorators.csrf import csrf_exempt


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
# So any user, even unauthenticated ones, can create a new user
@permission_classes([AllowAny])
@csrf_exempt
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # create the user 
        user = serializer.save()
        
        # generate jwt tokens for the user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        return Response({
            'access': access_token,
            'refresh': refresh_token,
            'user_id': user.id,
            'email': user.email,
            'username': user.username
        }, status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_routes(request):
    routes = [
        '/api/token',
        '/api/token/refresh'
    ]

    return Response(routes)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def files_handler(request):
    user = request.user

    if request.method == 'GET':
        files = user.file_set.all()
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        data['user'] = user.id  # Attach the user to the data
        serializer = FileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)  # 201: Created
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def file_detail_handler(request, file_id):
    user = request.user

    try:
        file_instance = user.file_set.get(id=file_id)
    except File.DoesNotExist:
        return Response({"detail": "File not found."}, status=404)

    if request.method == 'GET':
        serializer = FileSerializer(file_instance)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = FileSerializer(
            file_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        file_instance.delete()
        # 204: No Content
        return Response({"detail": "File deleted successfully."}, status=204)
