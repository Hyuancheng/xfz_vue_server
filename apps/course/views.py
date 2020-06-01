from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .models import Course


class CourseView(View):
    """用于展示课程"""

    def get(self, request):
        courses = Course.objects.only('id', 'teacher', 'cover_url', 'title', 'price').select_related('teacher')
        content = {
            'courses': courses
        }
        return render(request, 'course/course_index.html', content)


class CourseDetailView(View):
    """展示课程详情"""

    def get(self, request, course_id):
        try:
            course = Course.objects.filter(pk=course_id).select_related('teacher', 'category').first()
        except:
            return HttpResponse('页面不存在')

        content = {'course': course}
        return render(request, 'course/course_detail.html', content)
