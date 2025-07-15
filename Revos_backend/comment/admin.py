from django.contrib import admin
# from .models import Comment

# @admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'text', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('user', 'text')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
