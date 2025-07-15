from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('post/', include('article.urls')),
    path('get/', include('article.urls')),
    path('post/', include('vote.urls')),
    path('get/', include('vote.urls')),
    path('post/', include('comment.urls')),
    path('get/', include('comment.urls')),
    path('api/auth/', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
