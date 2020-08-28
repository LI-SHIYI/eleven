from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from blog.models import BlogsPost

def blog_index(request):
    blog_list = BlogsPost.objects.all()
    return render(request,'index.html',{'blog_list':blog_list})


def blog_contact(request):
    mobile =111111111
    return  render(request,'contact.html',{'mobile':mobile})