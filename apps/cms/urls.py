from django.urls import path
from . import views


app_name = 'cms'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('news/', views.NewsView.as_view(), name='news'),
    path('news_type/', views.NewsTypeView.as_view(), name='news_type'),
    path('news_img/', views.NewsImgView.as_view(), name='news_img'),
    path('news_list/', views.NewsListView.as_view(), name='news_list'),
    path('course_type/', views.CourseTypeView.as_view(), name='course_type'),
    path('course_detail/', views.CourseDetailView.as_view(), name='course'),
    path('course_list/', views.CourseListView.as_view(), name='course_list'),
    path('teacher/', views.TeacherView.as_view(), name='teacher'),
    path('teacher_list/', views.TeacherListView.as_view(), name='teacher_list'),
]
