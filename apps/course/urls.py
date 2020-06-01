from django.urls import path
from .views import CourseView, CourseDetailView

app_name = 'course'

urlpatterns = [
    path('', CourseView.as_view(), name='index'),
    path('detail/<int:course_id>/', CourseDetailView.as_view(), name='detail')
]
