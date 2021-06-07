from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, User, Comments
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from .forms import PostForm, CommentsAddForm
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

    return render(request, 'profile.html', {'posts': posts, 'u': user, 'paginator': paginator,
                                            'count': len(posts_lists)})


def post_views(request, username, post_id):
    """Страница отображения поста"""
    comments = Comments.objects.filter(post=post_id).order_by('-created').all()
    user = get_object_or_404(User, username=username)
    try:
        post = Post.objects.filter(author=user).get(pk=post_id)
        return render(request, 'post.html', {'post': post, 'items': comments})
    except ObjectDoesNotExist:
        return redirect('index')


@login_required
def post_edit(request, username, post_id):
    """Старница редактирования поста"""

    new = Post.objects.get(pk=post_id)
    if new.author == request.user:
        if request.method == "POST":
            form = PostForm(request.POST or None, files=request.FILES or None, instance=new)
            if form.is_valid():
                new.save()
                return redirect('post_view', username=username, post_id=post_id)
    else:
        return redirect('post_view', post_id=post_id, username=username)

    form = PostForm
    return render(request, 'post_edit.html', {'form': form})


@login_required
def new_post(request):
    """Страница создания поста"""

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.author = request.user
            new.save()
            return redirect('post_view', post_id=new.pk, username=new.author)
        return redirect('index')

    form = PostForm()
    return render(request, "new.html", {'form': form})


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию,
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


def add_comment(request, post_id, username):
    """Страница комментирования поста"""

    if request.method == "POST":
        form = CommentsAddForm(request.POST)
        post = Post.objects.get(pk=post_id)
        author = User.objects.get(username=request.user)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = author
            comment.post = post
            comment.save()
            return redirect('post_view', post_id=post_id, username=post.author)
        return redirect('post_view', post_id=post_id, username=post.author)
    form = CommentsAddForm()
    return redirect('index')
