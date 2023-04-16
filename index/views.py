from django.shortcuts import redirect, render
from django.http.response import JsonResponse
from django.http.request import HttpRequest
from django.http import HttpResponseRedirect
from django.urls.base import reverse
from auth.views import login_required
from urllib.parse import urlparse
# Create your views here.

# 渲染首页前端页面
def index(request):
    return render(request, 'index.html')