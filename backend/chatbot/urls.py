# In chatbot/urls.py
from django.urls import path
from .views import test_chatbot, ask_gpt  # Make sure 'ask_gpt' is defined as well

urlpatterns = [
    path('test/', test_chatbot, name='test_chatbot'),
    path('ask/', ask_gpt, name='ask_gpt'),  # Ensure ask_gpt exists too
]
