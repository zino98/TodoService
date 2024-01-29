from django.db import models

# Create your models here.
class Todo(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    done = models.BooleanField(default=False)  # 기본값 설정
    regdate = models.DateTimeField(auto_now_add=True)  # 오늘 날짜를 기본값으로 
    moddate = models.DateTimeField(null=True)  # 선택적으로 입력
