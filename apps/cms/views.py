from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from utils import json_code
from qiniu import Auth
from django.conf import settings
from django.db.utils import IntegrityError
# 新闻
from .forms import AddNewsTypeForm, ChangeNewsTypeForm, DeleteNewsTypeForm, NewsForm
from apps.news.models import NewsType, News
# 课程
from apps.course.models import Course, CourseCategory, Teacher
from apps.course.forms import CourseCategoryCreateForm, CourseCategoryChangeForm, CourseForm, TeacherForm

# 导入序列化器
from ..news.serializers import NewsSerializer, NewsTypeListSerializer, NewsListSerializer
from ..course.serializers import CourseTypeSerializer, CourseTypeListSerializer, CourseSerializer, TeacherSerializer, \
    CourseListSerializer, TeacherListSerializer

from django.db.models import Count
from rest_framework.renderers import JSONRenderer


# @method_decorator(staff_member_required(login_url='news:index'), name='dispatch')
class IndexView(View):
    """后台管理系统首页"""

    def get(self, request):
        return render(request, 'cms/index.html')


class NewsTypeView(View):
    """新闻分类"""

    def get(self, request):
        types = NewsType.objects.annotate(news_count=Count('news'))
        serialized = NewsTypeListSerializer(types, many=True)
        data = JSONRenderer().render(data=serialized.data).decode()
        return json_code.ok(data=data)

    def post(self, request):
        """新增新闻分类名称"""
        form = AddNewsTypeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd.get('name')
            new_category = NewsType.objects.create(name=name)

            # 将新增的分类返回客户端
            new_category.news_count = new_category.news_set.count()
            # 序列化
            serialized = NewsTypeListSerializer(new_category)
            data = JSONRenderer().render(data=serialized.data).decode()
            return json_code.ok('分类创建成功！', data=data)
        return json_code.params_error(form.get_error_data())

    def put(self, request):
        """修改新闻分类名称"""
        form = ChangeNewsTypeForm(request.PUT)
        if form.is_valid():
            cd = form.cleaned_data
            NewsType.objects.filter(pk=cd['type_id']).update(name=cd['name'])
            return json_code.ok('编辑成功！', data={'name': cd['name']})
        return json_code.params_error(form.get_error_data())

    def delete(self, request):
        """删除新闻分类"""
        form = DeleteNewsTypeForm(request.DELETE)
        if form.is_valid():
            cd = form.cleaned_data
            NewsType.objects.get(pk=cd['type_id']).delete()
            return json_code.ok('删除成功！')
        return json_code.params_error(form.get_error_data())


class NewsImgView(View):
    """返回上传图片到七牛云的token"""

    def get(self, request):
        # 需要填写你的 Access Key 和 Secret Key
        access_key = settings.QINIU_ACCESS_KEY
        secret_key = settings.QINIU_SECRET_KEY
        # 构建鉴权对象
        q = Auth(access_key, secret_key)
        # 要上传的空间
        bucket_name = settings.QINIU_BUCKET_NAME

        policy = {
            'callbackBody': 'filename=$(fname)'
        }
        # 3600为token过期时间，秒为单位。3600等于一小时
        token = q.upload_token(bucket_name, None, 3600, policy)

        return json_code.ok(data={'token': token})


class NewsView(View):
    """用于对新闻进行增删改查"""

    def get(self, request):
        """获取新闻"""
        new_id = request.GET.get('id')
        try:
            new = News.objects.get(pk=new_id)
        except:
            return json_code.params_error('该新闻不存在！')
        serialized = NewsSerializer(new)
        data = JSONRenderer().render(data=serialized.data).decode()
        return json_code.ok(data=data)

    def post(self, request):
        """发布新闻"""
        form = NewsForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            title = cd.get('title')
            author = request.user
            thumbnail = cd.get('thumbnail')
            des = cd.get('des')
            content = cd.get('content')
            category = NewsType.objects.get(pk=cd.get('category'))
            News.objects.create(title=title, author=author, thumbnail=thumbnail,
                                des=des, content=content, category=category)
            return json_code.ok('文章发布成功！')
        return json_code.params_error(form.get_error_data())

    def put(self, request):
        """修改新闻"""
        form = NewsForm(request.PUT)
        if form.is_valid():
            new_id = request.PUT.get('id')
            cd = form.cleaned_data
            title = cd.get('title')
            author = request.user
            thumbnail = cd.get('thumbnail')
            des = cd.get('des')
            content = cd.get('content')
            category = NewsType.objects.get(pk=cd.get('category'))
            if not new_id:
                return json_code.params_error('该新闻不存在！')
            News.objects.filter(pk=new_id).update(title=title, thumbnail=thumbnail, author=author,
                                                  des=des, content=content, category=category)
            return json_code.ok('文章修改成功！')
        return json_code.params_error(form.get_error_data())

    def delete(self, request):
        """删除新闻"""
        new_id = request.DELETE.get('id')
        try:
            News.objects.get(pk=new_id).delete()
        except:
            return json_code.params_error('该新闻不存在！')
        return json_code.ok()


class NewsListView(View):
    """获取新闻列表"""

    def get(self, request):
        """获取全部新闻组成的列表"""
        news = News.objects.only('author', 'id', 'category', 'title', 'pub_date').select_related('author', 'category')
        serialized = NewsListSerializer(news, many=True)
        data = JSONRenderer().render(data=serialized.data).decode()
        return json_code.ok(data=data)


class CourseTypeView(View):
    """课程分类"""

    def get(self, request):
        """获取新闻分类，无返回值"""
        course_types = CourseCategory.objects.annotate(course_count=Count('course'))
        serialized = CourseTypeListSerializer(course_types, many=True)
        data = JSONRenderer().render(data=serialized.data).decode()
        return json_code.ok(data=data)

    def post(self, request):
        """新增课程分类，返回新增分类的所有字段数据"""
        form = CourseCategoryCreateForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data.get('name')
            new_category = CourseCategory.objects.create(name=category_name)
            # 序列化并返回新建的课程分类
            serialized = CourseTypeSerializer(new_category)
            data = JSONRenderer().render(serialized.data).decode()
            return json_code.ok(data=data)
        else:
            return json_code.params_error(form.get_error_data())

    def put(self, request):
        """修改课程分类, 接收id, name两个参数， 返回修改后的分类名称"""
        form = CourseCategoryChangeForm(request.PUT)
        if form.is_valid():
            cd = form.cleaned_data
            category_id = cd.get('id')
            name = cd.get('name')
            CourseCategory.objects.filter(pk=category_id).update(name=name)
            data = {'name': name}
            return json_code.ok(data=data)
        else:
            json_code.params_error(form.get_error_data())

    def delete(self, request):
        """删除新闻分类，接收要删除的分类id作为参数,不返回被删除的课程分类信息"""
        category_id = request.DELETE.get('id')
        try:
            CourseCategory.objects.get(pk=category_id).delete()
        except IntegrityError:
            return json_code.params_error('无法删除含有课程的分类！')
        except:
            return json_code.params_error()
        return json_code.ok()


class TeacherView(View):
    """教师信息"""

    def get(self, request):
        """获取某名老师详细信息，接收该教师id作为参数"""
        teacher_id = request.GET.get('id')
        try:
            teacher = Teacher.objects.get(pk=teacher_id)
        except:
            return json_code.params_error('该教师不存在！')
        serialized = TeacherSerializer(teacher)
        data = JSONRenderer().render(serialized.data).decode()
        return json_code.ok(data=data)

    def post(self, request):
        """新建教师信息"""
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return json_code.ok()
        else:
            return json_code.params_error(form.get_error_data())

    def put(self, request):
        """修改教师信息"""
        teacher_id = request.PUT.get('id')
        try:
            teacher = Teacher.objects.get(pk=teacher_id)
        except:
            return json_code.params_error('该教师不存在！')
        form = TeacherForm(request.PUT, instance=teacher)
        if form.is_valid():
            form.save()
            return json_code.ok()
        else:
            return json_code.params_error(form.get_error_data())

    def delete(self, request):
        """删除教师信息"""
        teacher_id = request.DELETE.get('id')
        try:
            Teacher.objects.get(pk=teacher_id).delete()
        except IntegrityError:
            return json_code.params_error('无法删除拥有课程的教师！')
        except:
            return json_code.params_error('该教师不存在！')
        return json_code.ok()


class TeacherListView(View):
    """返回序列化后的教师列表"""

    def get(self, request):
        teachers = Teacher.objects.annotate(course_count=Count('course'))
        serialized = TeacherListSerializer(teachers, many=True)
        data = JSONRenderer().render(serialized.data).decode()
        return json_code.ok(data=data)


class CourseDetailView(View):
    """课程详情的增删改查"""

    def get(self, request):
        """查询单门课程，接收课程id作为参数，返回该门课程序列化后的值"""
        course_id = request.GET.get('id')
        try:
            course = Course.objects.filter(pk=course_id).select_related('teacher', 'category').first()
        except:
            return json_code.params_error('该课程不存在！')
        serialized = CourseSerializer(course)
        data = JSONRenderer().render(serialized.data).decode()
        return json_code.ok(data=data)

    def post(self, request):
        """发布课程"""
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return json_code.ok()
        else:
            return json_code.params_error(form.get_error_data())

    def put(self, request):
        """修改课程"""
        course_id = request.PUT.get('id')
        try:
            course = Course.objects.get(pk=course_id)
        except:
            return json_code.params_error('该课程不存在！')
        form = CourseForm(request.PUT, instance=course)
        if form.is_valid():
            form.save()
            return json_code.ok()
        return json_code.params_error(form.get_error_data())

    def delete(self, request):
        """删除课程"""
        course_id = request.DELETE.get('id')
        try:
            Course.objects.get(pk=course_id).delete()
        except:
            return json_code.params_error('该课程不存在！')
        return json_code.ok()


class CourseListView(View):
    """获取课程列表"""

    def get(self, request):
        """返回包含课程信息的字典组成的列表"""
        courses = Course.objects.only('id', 'title', 'teacher', 'category', 'price', 'pub_time').select_related(
            'teacher', 'category')
        serialized = CourseListSerializer(courses, many=True)
        data = JSONRenderer().render(serialized.data).decode()
        return json_code.ok(data=data)
