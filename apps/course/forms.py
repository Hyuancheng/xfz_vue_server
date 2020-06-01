from django import forms
from utils.form import FormMixin
from .models import Course, CourseCategory, Teacher, CourseOrder


class CourseCategoryCreateForm(forms.ModelForm, FormMixin):
    """新建课程分类的表单"""

    class Meta:
        model = CourseCategory
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data.get('name')
        exist = CourseCategory.objects.filter(name=name).exists()
        if exist:
            raise forms.ValidationError('该分类已存在！')
        return name


class CourseCategoryChangeForm(CourseCategoryCreateForm):
    """修改课程分类的表单"""
    id = forms.IntegerField()

    class Meta:
        model = CourseCategory
        fields = '__all__'

    def clean_id(self):
        course_id = self.cleaned_data.get('id')
        exist = Teacher.objects.get(pk=course_id).exists()
        if not exist:
            raise forms.ValidationError('该教师不存在！')
        return course_id


class TeacherForm(forms.ModelForm, FormMixin):
    """新建教师时用于验证的表单"""
    class Meta:
        model = Teacher
        fields = '__all__'


class CourseForm(forms.ModelForm, FormMixin):
    """用于创建课程"""

    class Meta:
        model = Course
        fields = '__all__'





