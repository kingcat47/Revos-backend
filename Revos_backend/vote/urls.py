# vote/urls.py
from django.urls import path
from .views import create_votes, get_votes_by_article, submit_vote

urlpatterns = [
    path('vote/create', create_votes, name='create_votes'),
    path('votes_by_article/<str:article_id>/', get_votes_by_article, name='get_votes_by_article'),
    path('vote/submit', submit_vote, name='submit_vote'),
]