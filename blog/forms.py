from django import forms
from .models import Post


#  Modelform 상속받는 PostModelform 클래스 정의
class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', )
