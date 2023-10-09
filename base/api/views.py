from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


from .serializers import FileSerializer
from base.models import File


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


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh'
    ]

    return Response(routes)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filesHandler(request):
    user = request.user
    
    if request.method == 'GET':
        files = user.file_set.all()
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data
        data['user'] = user.id # Attach the user to the data
        serializer = FileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201) # 201: Created
        return Response(serializer.errors, status=400)
    

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def fileDetailHandler(request, file_id):
    user = request.user
    
    try:
        file_instance = user.file_set.get(id=file_id)
    except File.DoesNotExist:
        return Response({"detail": "File not found."}, status=404)
    
    if request.method == 'GET':
        serializer = FileSerializer(file_instance)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = FileSerializer(file_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        file_instance.delete()
        return Response({"detail": "File deleted successfully."}, status=204) # 204: No Content
