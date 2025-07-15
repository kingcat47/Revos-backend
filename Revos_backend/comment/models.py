from django.db import models
from vote.models import Question
from accounts.models import User  # User 모델 import

class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')  # ForeignKey로 변경
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username}: {self.text[:50]}'