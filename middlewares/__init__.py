import simplejson
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from django.http.request import HttpRequest
from django.contrib.auth.models import User


class AccessTokenMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest):
        id_ = request.headers.get("access-token")
        if id_:
            user = User.objects.filter(id=id_).first()
            if user:
                request.user = user


class JsonMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest):
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
