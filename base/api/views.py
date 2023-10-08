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
def getNotes(request):
    user = request.user
    notes = user.file_set.all()
    serializer = FileSerializer(notes, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateNote(request, note_id):
    user = request.user 
    try: 
        note = user.file_set.get(id=note_id)
    except File.DoesNotExist:
        return Response({"detail": "Note not found."}, status = 404)
    
    if request.method == 'POST':
        serializer = FileSerializer(note, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save() # This will update the note.
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    return Response({"detail": "Invalid method."}, status=405)
