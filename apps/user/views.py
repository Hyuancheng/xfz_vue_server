from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login
from io import BytesIO
import random
from django_redis import get_redis_connection

from .forms import LoginForm, SendCodeForm, RegisterForm
from .models import MyUser
from utils import json_code
from utils.captcha.xfzcaptcha import Captcha
from utils.aliyunsms import aliyunsms


class LoginView(View):

    def post(self, request):
        """登录视图"""
        form = LoginForm(request.POST)
        if form.is_valid():
            # 提取数据
            cd = form.cleaned_data
            telephone = cd.get('telephone')
            password = cd.get('password')
            remember = cd.get('remember')
            # 验证用户
            user = authenticate(request, telephone=telephone, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    if remember:
                        request.session.set_expiry(None)
                    else:
                        request.session.set_expiry(0)
                    data = {
                        'username': user.username
                    }
                    return json_code.ok(data=data)
                else:
                    return json_code.auth_deny(message='该账号已冻结')
            else:
                return json_code.auth_deny(message='账号或密码错误')
        else:
            return json_code.auth_deny(message='账号或密码错误')


class RegisterView(View):

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd.get('username')
            telephone = cd.get('telephone')
            password = cd.get('password1')
            user = MyUser.objects.create_user(username=username, telephone=telephone)
            user.set_password(password)
            return json_code.ok(message='注册成功')
        else:
            return json_code.params_error(message=form.get_error_data())


def img_captcha(request):
    text, image = Captcha.gene_code()

    # 在缓存中保存图片验证码,20分钟后自动过期
    cache = get_redis_connection('default')
    cache.set(text.lower(), text.lower(), ex=1200)

    # BytesIO：相当于一个管道，用来存储图片的流数据
    out = BytesIO()
    # 调用image的save方法，将这个image对象保存到BytesIO中
    image.save(out, 'png')
    # 将BytesIO的文件指针移动到最开始的位置
    out.seek(0)

    response = HttpResponse(content_type='image/png')
    # 从BytesIO的管道中，读取出图片数据，保存到response对象上
    response.write(out.read())
    response['Content-length'] = out.tell()

    # 12Df：12Df.lower()
    # cache.set(text.lower(),text.lower(),5*60)
    return response


# /user/code/
def send_code(request):
    """发送短信验证码,将验证码保存在缓存中"""
    form = SendCodeForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        phone_code = str(random.random())[-6:]
        response = aliyunsms.send_msg(telephone, phone_code)
        # 将验证码有效期设置为10分钟，并以字符串的形式保存到缓存中
        cache = get_redis_connection('default')
        cache.set(telephone, phone_code, ex=600)

        return json_code.ok()
    else:
        return json_code.params_error(message='手机号码不正确')
