from rest_framework import generics, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Note
from .paginations import NotesAPIListPagination
from .permissions import IsOwner
from .serializers import NoteSerializer


class NoteListAPI(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOwner, IsAuthenticated)
    pagination_class = NotesAPIListPagination
    serializer_class = NoteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('title',)

    def get_queryset(self):
        user_id = self.request.user.id
        return Note.objects.filter(user_id=user_id)

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


class RetrieveNoteAPI(generics.RetrieveAPIView):
    queryset = Note.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOwner, IsAuthenticated)
    serializer_class = NoteSerializer


class AddNoteAPI(generics.CreateAPIView):
    queryset = Note.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOwner, IsAuthenticated)
    serializer_class = NoteSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


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
