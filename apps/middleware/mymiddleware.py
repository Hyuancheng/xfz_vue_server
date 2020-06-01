from django.http import QueryDict


class MethodMiddleware:
    """该中间件用于将PUT, DELETE请求方法的参数附加到request对象上"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'PUT':
            request.PUT = QueryDict(request.body)
        elif request.method == 'DELETE':
            request.DELETE = QueryDict(request.body)
        response = self.get_response(request)
        return response



