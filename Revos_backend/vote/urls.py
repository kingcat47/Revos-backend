# vote/urls.py
from django.urls import path
from .views import create_votes

urlpatterns = [
    path('vote/create', create_votes, name='create_votes'),
]