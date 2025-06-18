from django.db import models
from django.utils import timezone
from datetime import timedelta
from article.models import Article

class Question(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=100)
    expired_data = models.DateTimeField('expired data', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # 마감일이 설정되지 않은 경우 자동으로 일주일 후로 설정
        if not self.expired_data:
            self.expired_data = timezone.now() + timedelta(days=7)
        super().save(*args, **kwargs)

    def is_expired(self):
        """투표가 마감되었는지 확인"""
        if not self.expired_data:
            return False
        return timezone.now() > self.expired_data

    def days_remaining(self):
        """마감까지 남은 일수 반환"""
        if not self.expired_data:
            return None
        if self.is_expired():
            return 0
        remaining = self.expired_data - timezone.now()
        return remaining.days

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text