from django.http import HttpResponse, JsonResponse
import json


class JsonCode:
    """返回给前端的状态码"""

    ok = 200                # 正常
    params_error = 400      # 参数错误
    auth_deny = 401         # 认证失败
    method_error = 405      # 方法错误
    server_error = 500      # 服务器错误


def _result(code=JsonCode.ok, message=None, data=None, **kwargs):
    json_dict = {'code': code, 'message': message, 'data': data}

    if kwargs:
        json_dict.update(kwargs)
    print(json_dict)
    return JsonResponse(json_dict)


def ok(message='请求成功', data=None, **kwargs):
    return _result(code=JsonCode.ok, message=message, data=data, **kwargs)


def params_error(message='参数错误', data=None, **kwargs):
    return _result(code=JsonCode.params_error, message=message, data=data, **kwargs)


def auth_deny(message='用户验证失败', data=None, **kwargs):
    return _result(code=JsonCode.auth_deny, message=message, data=data, **kwargs)


def method_error(message='请求方法错误', data=None, **kwargs):
    return _result(code=JsonCode.method_error, message=message, data=data, **kwargs)


def server_error(message='服务器错误', data=None, **kwargs):
    return _result(code=JsonCode.server_error, message=message, data=data, **kwargs)




