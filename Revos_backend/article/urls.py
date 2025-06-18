from django.urls import path
from .views import create_article, get_all_articles, get_article_by_id

urlpatterns = [
    path('create', create_article, name='create_article'),
    path('get_all_article', get_all_articles, name='get_all_articles'),
    path('get_article_by_id', get_article_by_id, name='get_article_by_id'),
]
