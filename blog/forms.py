from django import forms
from .models import Post, Comment


# ModelForm을 상속받는 CommenModelForm 클래스 정의
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)


#  Modelform 상속받는 PostModelform 클래스 정의
class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', )


def min_length_5_validator(value):
    if len(value) < 5:
        # ValidatorError 예외 강제로 발생시킴
        raise forms.ValidationError('text는 5글자 이상 입력해주세요!')


# Form을 상속받는 PostForm 클래스 정의
class PostForm(forms.Form):
    title = forms.CharField()
    text = forms.CharField(widget=forms.Textarea, validators=[min_length_5_validator])