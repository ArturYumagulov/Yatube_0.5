from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, User, Comments, Follow
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from .forms import PostForm, CommentsAddForm, FollowForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page


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


@login_required
def profile(request, username):
    """Страница с профилем пользователя"""

    user = get_object_or_404(User, username=username)
    posts_lists = Post.objects.filter(author=user).order_by('-pub_date').all()
    paginator = Paginator(posts_lists, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    following = request.user.follower.filter(author=user).exists()

    return render(request, 'profile.html', {'posts': posts, 'u': user, 'paginator': paginator,
                                            'count': len(posts_lists), "following": following, 'username': username})


def post_views(request, username, post_id):
    """Страница отображения поста"""
    comments = Comments.objects.filter(post=post_id).order_by('-created').all()
    user = get_object_or_404(User, username=username)
    queryset = Post.objects.filter(author=user)
    post = get_object_or_404(queryset, pk=post_id)
    return render(request, 'post.html', {'post': post, 'items': comments})


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


@login_required
def add_comment(request, post_id, username):
    """Страница комментирования поста"""

    form = CommentsAddForm(request.POST)
    post = Post.objects.get(pk=post_id)
    author = User.objects.get(username=request.user)
    if request.method == "POST":
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = author
            comment.post = post
            comment.save()
            return redirect('post_view', post_id=post_id, username=post.author)
        return redirect('post_view', post_id=post_id, username=post.author)
    form = CommentsAddForm()
    return redirect('post_view', post_id=post_id, username=post.author)


@login_required
def follow_index(request):
    """Вывод постов подписанных авторов"""

    user_follows = get_object_or_404(User, pk=request.user.id).follower.all().values_list('author')
    posts_list = Post.objects.filter(author__in=user_follows).order_by('-pub_date').all()
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    pages = paginator.get_page(page_number)
    return render(request, 'follow.html', {'posts': pages, 'paginator': paginator})


@login_required
def profile_follow(request, username):
    """Подписка на автора"""

    user = get_object_or_404(User, username=request.user.username)
    author = get_object_or_404(User, username=username)
    follower = Follow.objects.create(author=author, user=user)
    if request.method == "POST":
        form = FollowForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile', username=username)
    follower.save()
    return redirect('profile', username=username)


def profile_unfollow(request, username):
    """Отписка от автора"""

    user = get_object_or_404(User, username=request.user.username)
    author = get_object_or_404(User, username=username)
    if request.method == "POST":
        form = FollowForm(request.POST)
        if form.is_valid():
            form.delete()
            return redirect('profile', username=username)
    else:
        follow = Follow.objects.get(author=author, user=user)
        follow.delete()
        return redirect('profile', username=username)
