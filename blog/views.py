from django.shortcuts import render
from django.utils import timezone
from blog.models import Post
import blog.views
import blog.models

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})