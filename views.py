from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .models import Post
from .forms import PostForm


def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home/home.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'home/post_detail.html', {'post': post})


@require_http_methods(["GET", "POST"])
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'home/create_post.html', {'form': form})


@require_http_methods(["GET", "POST"])
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'home/edit_post.html', {'form': form, 'post': post})


@require_http_methods(["GET", "POST"])
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'home/post_detail.html', {'post': post})
