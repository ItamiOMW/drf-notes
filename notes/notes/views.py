from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Note
from .permissions import IsOwner
from .serializers import NoteSerializer


class NotesAPIListPagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'page_size'
    max_page_size = 100


class NoteListAPI(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOwner, IsAuthenticated)

    def list(self, request, *args, **kwargs):
        user_id = Token.objects.get(key=request.auth.key).user_id
        queryset = Note.objects.filter(user=user_id)
        serializer = NoteSerializer(queryset, many=True)
        return Response(serializer.data)


class AddNoteAPI(generics.CreateAPIView):
    queryset = Note.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOwner, IsAuthenticated)
    serializer_class = NoteSerializer


class UpdateNoteAPI(generics.UpdateAPIView):
    queryset = Note.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOwner, IsAuthenticated)
    serializer_class = NoteSerializer


class DeleteNoteAPI(generics.DestroyAPIView):
    queryset = Note.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOwner, IsAuthenticated)
    serializer_class = NoteSerializer
