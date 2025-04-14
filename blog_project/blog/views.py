from django.core.paginator import Paginator
from django.db import IntegrityError
from django.shortcuts import render, redirect
from blog.models import Post, Comment, User
from .forms import PostForm, CommentForm
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .serializers import PostSerializer, CommentSerializer
from django.http import HttpResponseForbidden

def home(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "title": "Главная страница блога",
        "description": "Описание",
        "paginator": paginator,
        "page_number": page_number,
    }
    return render(request, "partial/home.html", context)


def article(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect('single_article', pk=post.pk)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form
    }
    return render(request, "partial/single_article.html", context)


def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            image = form.cleaned_data['image']
            author = form.cleaned_data['author']

            try:
                user = User.objects.get(username=author)
            except User.DoesNotExist:
                user = User.objects.create_user(username=author, password=None)

            post = Post.objects.create(
                title=title,
                content=content,
                image=image,
                author=user
            )

        return redirect('home')
    else:
        form = PostForm()
    return render(request, 'partial/add_post.html', {'form': form})


def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("Вы не автор данного поста!")
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            updated_post = form.save()
            return redirect('single_article', pk=updated_post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'partial/add_post.html', {'form': form, 'post': post})

def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("Вы не автор данного поста!")

    if request.method == 'POST':
        post.delete()
        return redirect('home')

    return render(request, 'partial/delete_post.html', {'post': post})
# ViewSets

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
