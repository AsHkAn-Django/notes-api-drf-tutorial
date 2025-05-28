from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Note
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse


User = get_user_model()


class NoteModelTest(TestCase):
    
    def test_note_str(self):
        user = User.objects.create_user(username='test1', password='pass')
        note = Note.objects.create(title='Note Note', body='Note Body', owner=user)
        self.assertEqual(str(note), 'Note Note')


class NoteAPITest(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='test1', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.note = Note.objects.create(title='Note Note', body='Note Body', owner=self.user)
        
    def test_list_note(self):
        response = self.client.get('/api/notes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  
        
    def test_create_note(self):
        data = {'title': 'New Note', 'body': 'New Body'}
        response = self.client.post('/api/notes/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 2)
        
    def test_get_signal_note(self):
        response = self.client.get(f'/api/notes/{self.note.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Note Note')
        
    def test_update_task(self):
        data = {'title': 'Updated', 'body': 'Body'}
        response = self.client.put(f'/api/notes/{self.note.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Updated')
        self.assertEqual(self.note.body, 'Body')
        
    def test_delete_task(self):
        response = self.client.delete(f'/api/notes/{self.note.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Note.objects.count(), 0)
        
    def test_filter_title(self):
        response = self.client.get('/api/notes/?title=note')
        self.assertEqual(len(response.data), 1)
    
    def test_auth_required(self):
        # Unauthenticated users should not be able to update notes
        self.client.logout()
        data = {'title': 'Updated', 'body': 'Body'}
        response = self.client.put(f'/api/notes/{self.note.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)