from django.contrib import admin
from .models import Question, Choice

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'article', 'expired_data', 'is_expired_display', 'days_remaining_display', 'created_at')
    list_filter = ('expired_data', 'created_at')
    search_fields = ('question_text',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def is_expired_display(self, obj):
        """마감 상태를 표시"""
        if not obj.expired_data:
            return "마감일 미설정"
        if obj.is_expired():
            return "마감됨"
        return "진행중"
    is_expired_display.short_description = "마감 상태"

    def days_remaining_display(self, obj):
        """남은 일수를 표시"""
        if not obj.expired_data:
            return "마감일 미설정"
        days = obj.days_remaining()
        if days == 0:
            return "마감됨"
        return f"{days}일 남음"
    days_remaining_display.short_description = "남은 일수"

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'question', 'votes')
    list_filter = ('votes',)
    search_fields = ('choice_text',)
    ordering = ('-votes',) 