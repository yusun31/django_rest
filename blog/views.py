from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Post, Comment
from .forms import PostModelForm, PostForm, CommentForm


# 댓글 승인
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


# 댓글 삭제
@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)


# 댓글 등록
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
# 글 삭제
def post_remove(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('post_list_home')


@login_required
# 글 수정(ModelForm 사용)
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostModelForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostModelForm(instance=post)
    return render(request, 'blog/post_edit.html', {'postform': form})


@login_required
# 글 등록(Form 사용)
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            clean_data_dict = form.cleaned_data
            # create() 함수가 호출되면 등록처리가 이루어짐
            post = Post.objects.create(
                author=request.user,
                title=clean_data_dict['title'],
                text=clean_data_dict['text'],
                published_date=timezone.now()
            )
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'postform': form})


# 글 등록(ModelForm 사용)
def post_new_modelform(request):
    if request.method == "POST":
        # 등록 요청(등록버튼을 눌렀을 경우)
        post_form = PostModelForm(request.POST)
        if post_form.is_valid():  # 검증 logic을 통과하면
            # form 객체의 save 를 호출하면 Model 객체 생성
            post = post_form.save(commit=False)  # commit=False : 바로 저장하지 않음
            # 로그인된 username -> 작성자(author) 필드에 저장
            post.author = request.user
            # 현재 날짜와 시간을 게시일자(published_date) 필드에 저장
            post.published_date = timezone.now()
            # post 객체가 저장 + insert
            post.save()
            # 등록 후 상세페이지로 바로 이동
            return redirect('post_detail', pk=post.pk)
    else:
        # 등록을 하기 위한 form 띄우기
        post_form = PostModelForm()
    return render(request, 'blog/post_edit.html', {'postform': post_form})


# 글 상세정보
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post_key': post})


# 글 목록(Post list)
def post_list(request):
    # Create your views here.
    # Views 내에 선언된 함수 -> 인자로 HttpRequest 라는 객체를 Django 가 전달
    my_name = '장고웹프레임워크'
    http_method = request.method
    # return HttpResponse('''
    #     <h2> Welcome {name}</h2>
    #     <p> Http Method : {method} </p>
    #     <p> Http headers User-Agent : {header} </p>
    #     <p> Http Path : {my_path} </p>
    # '''.format(name=my_name, method=http_method, header=request.headers['user-agent'], my_path=request.path))
    # return render(request, 'blog/post_list.html')
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'post_list': posts})
