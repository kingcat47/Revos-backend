from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')  # 목록에서 보여줄 필드
    list_filter = ('category', 'created_at')  # 필터링할 수 있는 필드
    search_fields = ('title', 'text')  # 검색할 수 있는 필드
    ordering = ('-created_at',)  # 기본 정렬 순서 