from django import forms
from apps.news.models import NewsType
from utils.form import FormMixin
from apps.news.models import News


class AddNewsTypeForm(forms.ModelForm, FormMixin):
    """新增新闻分类的表单"""

    class Meta:
        model = NewsType
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        exist = NewsType.objects.filter(name=name).exists()
        if exist:
            raise forms.ValidationError('该分类已存在！')
        return name


class ChangeNewsTypeForm(forms.ModelForm, FormMixin):
    """修改新闻分类的表单"""
    type_id = forms.CharField(max_length=10)

    class Meta:
        model = NewsType
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        exist = NewsType.objects.filter(name=name).exists()
        if exist:
            raise forms.ValidationError('该分类已存在！')
        return name

    def clean_type_id(self):
        type_id = self.cleaned_data.get('type_id')
        exist = NewsType.objects.filter(pk=type_id).exists()
        if not exist:
            raise forms.ValidationError('编辑的分类不存在！')
        return type_id


class DeleteNewsTypeForm(forms.Form, FormMixin):
    """删除新闻分类的表单"""
    type_id = forms.CharField(max_length=10)

    def clean_type_id(self):
        cd = self.cleaned_data
        type_id = cd.get('type_id')
        exist = NewsType.objects.filter(pk=type_id).exists()
        if not exist:
            raise forms.ValidationError('删除的分类不存在！')
        return type_id


class NewsImgForm(forms.Form, FormMixin):
    """验证图片的格式"""
    img = forms.ImageField()

    def clean_img(self):
        cd = self.cleaned_data
        img = cd.get('img')
        if not img.image.format.lower() in ['png', 'jpg', 'gif', 'jpeg']:
            raise forms.ValidationError('图片格式不正确，仅支持"png"格式！')
        return img


class NewsForm(forms.ModelForm, FormMixin):
    category = forms.IntegerField()

    class Meta:
        model = News
        exclude = ['author', 'category', 'pub_date']

    def clean_category(self):
        category_id = self.cleaned_data.get('category')
        try:
            NewsType.objects.get(pk=category_id)
        except:
            raise forms.ValidationError('该分类不存在！')
        return category_id

