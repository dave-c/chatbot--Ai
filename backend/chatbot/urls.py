from django.urls import path
from .views import ask_gpt, generate_quiz, scan_notes

urlpatterns = [
    path('ask/', ask_gpt, name='ask_gpt'),
    path('quiz/', generate_quiz, name='generate_quiz'),
    path('scan/', scan_notes, name='scan_notes'),
]
