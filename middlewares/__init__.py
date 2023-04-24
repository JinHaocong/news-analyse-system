import simplejson
from django.contrib.auth.models import User
from django.http.request import HttpRequest
from django.utils.deprecation import MiddlewareMixin

"""
Django中间件
AccessTokenMiddleware类会在每次请求进来时检查HTTP请求头中是否有access-token，
如果有的话，会根据该access-token找到对应的用户，并将该用户赋值给request.user属性。
这样，后续的视图函数或其他中间件就可以通过request.user来获取当前用户了。

JsonMiddleware类会在每次请求进来时检查请求参数，并尝试将其解析成JSON格式的数据。
如果请求的方法是POST，会尝试从请求体中获取JSON数据；
如果请求的方法是GET，会尝试从URL中获取JSON数据。如果无法解析成JSON数据，则会将空字典赋值给request.json属性。
"""


class AccessTokenMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request: HttpRequest):
        id_ = request.headers.get("access-token")
        if id_:
            user = User.objects.filter(id=id_).first()
            if user:
                request.user = user


class JsonMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request: HttpRequest):
        try:
            if request.method == "POST":
                try:
                    data = simplejson.loads(request.body)
                except:
                    data = request.POST
            else:
                data = request.GET
        except:
            data = {}
        request.json = data
