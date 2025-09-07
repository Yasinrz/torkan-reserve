from django.shortcuts import render , get_object_or_404
from .models import *
# Create your views here.


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, status="published")

    context = {
        "article": article,
        "likes_count": article.likes_count,
        "comments": article.comments.filter(is_approved=True),
        "comments_count": article.comments_count,
    }
    return render(request, "article/list_article.html", context)


def gallery(request):
    images = Gallery.objects.filter(status=True).order_by("-created_at")
    return render(request, "article/gallery.html", {"images": images})