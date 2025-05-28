from rest_framework import generics

from .models import Note
from .serializers import NoteSerializer
from .permissions import IsOwner



class NoteList(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        

class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsOwner,)
