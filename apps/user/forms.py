from django import forms
from utils.form import FormMixin
from .models import MyUser
import re
from django_redis import get_redis_connection


class LoginForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11, min_length=11, error_messages={
        'max_length': '手机号码位数不正确',
        'required': '手机号码不能为空',
        'min_length': '手机号码位数不正确'
    })
    password = forms.CharField(max_length=16, error_messages={'required': '密码不能为空'})
    remember = forms.IntegerField(required=False)


class RegisterForm(forms.Form, FormMixin):
    username = forms.CharField(max_length=16, min_length=2, required=True)
    telephone = forms.CharField(max_length=11, min_length=11, required=True)
    password1 = forms.CharField(max_length=16, min_length=6)
    password2 = forms.CharField(max_length=16, min_length=6)
    img_code = forms.CharField(max_length=4, min_length=4)
    sms_code = forms.CharField(max_length=6, min_length=6)

    def clean(self):
        cd = super().clean()
        if cd.get('password1') != cd.get('password2'):
            raise forms.ValidationError('两次密码输入不一致')

        ret = re.match(r"^1[35678]\d{9}$", cd.get('telephone', 'error'))
        if not ret:
            raise forms.ValidationError('请输入有效手机号码！')

        exist1 = MyUser.objects.filter(telephone=cd.get('telephone')).exists()
        if exist1:
            raise forms.ValidationError('该手机号码已注册！')

        exist2 = MyUser.objects.filter(username=cd.get('username')).exists()
        if exist2:
            raise forms.ValidationError('用户名已存在！')

        cache = get_redis_connection('default')
        img_code = cd.get('img_code').lower()
        img_cache = cache.get(img_code)
        if not img_cache:
            raise forms.ValidationError('图片验证码不正确！')

        phone_code = cache.get(cd.get('telephone')).decode()
        if phone_code != str(cd.get('sms_code')):
            raise forms.ValidationError('短信验证码不正确！')
        return cd


class SendCodeForm(forms.Form, FormMixin):
    """用户获取短信验证码时，该表单将验证手机号码的合法性"""
    telephone = forms.CharField(max_length=11, min_length=11, required=True)

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        ret = re.match(r"^1[35678]\d{9}$", telephone)
        if not ret:
            raise forms.ValidationError('请输入有效手机号码！')
        return telephone

