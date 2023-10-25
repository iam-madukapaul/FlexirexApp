from django.shortcuts import render, get_object_or_404
from .models import Post
from .models import Home
import random


# Create your views here.
def index(request):
    posts = Post.objects.all().order_by('-time')
    home_data_list = Home.objects.all()
    random_online_user = random.randint(4000, 6000)
    context = {
        'posts':posts,
        'home_data_list': home_data_list,
        'random_online_user': random_online_user,
    }
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

def affiliate(request):
    return render(request, 'affiliate.html')

def faq(request):
    return render(request, 'faq.html')

def policy(request):
    return render(request, 'policy.html')

def detail_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    posts = Post.objects.all().order_by('-time')
    context = {
        'post':post,
        'posts':posts,
    }
    return render(request, 'detail_post.html', context)

def plan(request):
    return render(request, 'plan.html')
