from django.urls import path
from .views import *

urlpatterns = [
    path("user", get_user_view, name="get_user"),  # 获取用户信息
    path("user/login", login_view, name="user_login"),  # 登录
    path("user/register", signup, name="user_signup"),  # 注册
    # path('logout/', logout_view, name='user_logout'), # 退出登录
]
