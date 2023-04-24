from django.shortcuts import render


# Create your views here.

# 渲染首页前端页面
def index(request):
    return render(request, 'index.html')
