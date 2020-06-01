from rest_framework import serializers
from .models import Course, CourseCategory, Teacher


class CourseTypeListSerializer(serializers.ModelSerializer):
    """序列化课程分类组成的列表"""
    course_count = serializers.IntegerField()

    class Meta:
        model = CourseCategory
        fields = '__all__'


class CourseTypeSerializer(serializers.ModelSerializer):
    """序列化单个课程分类"""

    class Meta:
        model = CourseCategory
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    """序列化单名教师信息"""

    class Meta:
        model = Teacher
        fields = '__all__'


class TeacherListSerializer(serializers.ModelSerializer):
    """序列化教师列表，包含每位教师拥有的课程数量"""
    course_count = serializers.IntegerField()

    class Meta:
        model = Teacher
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    """序列化单个课程详细信息"""
    teacher = TeacherSerializer()
    category = CourseTypeSerializer()

    class Meta:
        model = Course
        fields = '__all__'


class CourseListSerializer(serializers.ModelSerializer):
    """序列化课程列表，此处只序列化'id', 'category', 'teacher', 'title', 'price'五个字段用于展示"""
    teacher = serializers.SlugRelatedField(slug_field='username', read_only=True)
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'category', 'teacher', 'title', 'price', 'pub_time')



