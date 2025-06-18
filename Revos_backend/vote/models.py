from django.db import models
from article.models import Article

class Vote(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='votes')
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title 