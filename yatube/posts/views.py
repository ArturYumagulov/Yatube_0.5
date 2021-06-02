from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, User
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from .forms import PostForm
from django.contrib.auth.decorators import login_required


def index(request):
    """Отображение главной страницы"""

    post_lists = Post.objects.order_by("-pub_date").all()
    paginator = Paginator(post_lists, 10)
    page_number = request.GET.get('page')
    pages = paginator.get_page(page_number)
    return render(request, "index.html", {"posts": pages, 'paginator': paginator})


def group_posts(request, slug):
    """Группировка записей по автору"""

    group = get_object_or_404(Group, slug=slug)
    posts_lists = Post.objects.filter(group=group).order_by("-pub_date").all()
    paginator = Paginator(posts_lists, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, "group.html", {"group": group, "posts": posts, 'paginator': paginator})


def profile(request, username):
    """Страница с профилем пользователя"""

    user = get_object_or_404(User, username=username)
    posts_lists = Post.objects.filter(author=user).order_by('-pub_date').all()
    paginator = Paginator(posts_lists, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'profile.html', {'posts': posts, 'u': user,'paginator': paginator,
                                            'count': len(posts_lists)})


def post_views(request, username, post_id):
    """Страница отображения поста"""

    user = get_object_or_404(User, username=username)
    try:
        post = Post.objects.filter(author=user).get(pk=post_id)
        return render(request, 'post.html', {'post': post})
    except ObjectDoesNotExist:
        return redirect('index')


@login_required
def post_edit(request, username, post_id):
    """Старница редактирования поста"""

    new = Post.objects.get(pk=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=new)
        if form.is_valid():
            new.save()
            return redirect('index')

    form = PostForm
    return render(request, 'post_edit.html', {'form': form})
