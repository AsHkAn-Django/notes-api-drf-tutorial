from rest_framework import generics

from .models import Note
from .serializers import NoteSerializer
from .permissions import IsOwner



class NoteList(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
    def get_queryset(self):
        querryset = Note.objects.all()
        title = self.request.query_params.get('title')
        
        if title:
            querryset = querryset.filter(title__icontains=title)
        
        return querryset
        

class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsOwner,)
