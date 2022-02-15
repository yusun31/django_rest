from django.db import models
from django.utils import timezone
from django import forms


# title 필드의 length가 2보다 작으면 검증오류를 발생시키는 함수
def min_length_2_validator(value):
    if len(value) < 2:
        # ValidatorError 예외 강제로 발생시킴
        raise forms.ValidationError('title은 2글자 이상 입력해주세요!')


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, validators=[min_length_2_validator])
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    # 삭제할 예정 migration 테스트
    # test = models.TextField()

    # published date 필드에 현재 날짜를 저장하는 method
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    # Model 클래스에 정의된 __str__함수를 재정의(title 필드값을 리턴)
    def __str__(self):
        return self.title + '(' + str(self.id) + ')'
