from django.db import models

class Article(models.Model):

    #  카테고리 선택지를 지정해두는 상수 (관리자 페이지나 입력폼에서 선택 제한)
    CATEGORY_CHOICES = [
        ('스포츠', '스포츠'),  # (저장될 값, 사용자에게 보여지는 값)
        ('교육', '교육'),
        ('사회', '사회'),
        ('경제', '경제'),
    ]

    title = models.CharField(max_length=18)
    text = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    img = models.ImageField(upload_to='uploads/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

