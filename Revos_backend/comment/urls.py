from django.urls import path
from .views import get_comments, create_comment

urlpatterns = [
    path('comments/<str:vote_id>', get_comments, name='get_comments'),
    path('comment/', create_comment, name='create_comment'),
]
