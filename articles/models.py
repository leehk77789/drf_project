from django.db import models
from users.models import User

# Create your models here.
class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    #미디어파일 업로드 위치설정
    image = models.ImageField(blank=True, upload_to='%Y/%m/')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    likes = models.ManyToManyField(User, related_name="like_articles")

    def __str__(self):
        return str(self.title)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #Aricle을 foreignkey로 가져옴
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comment_set')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.content)