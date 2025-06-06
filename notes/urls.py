from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.NoteList.as_view(), name='note-list'),
    path('<int:pk>/', views.NoteDetail.as_view(), name='note-detail'),
]