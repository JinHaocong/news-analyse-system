from re import U
import simplejson
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http.request import HttpRequest
from index.utils import success, error
from functools import wraps
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse

# 用户登录装饰器，用于限制必须登录的情况
def login_required(func):
    @wraps(func)
    def wrap(request: HttpRequest, *args, **kwargs):
        # 如果用户已登陆，允许访问
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        return error(code=401)

    return wrap


# 用户登录视图
def login_view(request: HttpRequest):
    data = simplejson.loads(request.body)
    user = authenticate(
        request, username=data.get("username"), password=data.get("password")
    )
    if user:
        # 账号密码成功，进入主页面
        return success(data=user.id)
    return error("帐号或密码错误")


@login_required
def get_user_view(request: HttpRequest):
    id_ = request.headers.get("access-token")
    user = User.objects.filter(id=id_).first()
    if user:
        return success(
            data={"name": user.username, "role": [], "isSuperuser": user.is_superuser}
        )


# 用户注册视图
def signup(request):
    data = simplejson.loads(request.body)
    if not all((data.get("username"), data.get("password"), data.get("password2"))):
        return error("信息不全")
    if data.get("password") != data.get("password2"):
        return error("二次密码不一致")
    if User.objects.filter(username=data.get("username")).exists():
        return error("帐号已存在")
    user = User.objects.create_user(
        username=data.get("username"), password=data.get("password"), is_staff=True
    )  # , is_superuser=True
    # 注册新用户
    user.save()
    return success(data=user.id)


# 工具函数
def to_dict(l):
    def _todict(obj):
        j = {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
        return j

    return [_todict(i) for i in l]
