from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Post, Group
from django.core.paginator import Paginator


def index(request):
    post_lists = Post.objects.order_by("-pub_date").all()
    paginator = Paginator(post_lists, 10)
    page_number = request.GET.get('page')
    pages = paginator.get_page(page_number)
    return render(request, "index.html", {"posts": pages, 'paginator': paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts_lists = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    paginator = Paginator(posts_lists, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, "group.html", {"group": group, "posts": posts, 'paginator': paginator})
