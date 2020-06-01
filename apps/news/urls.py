from django.urls import path
from . import views


app_name = 'news'
urlpatterns = [
    # path('index/', views.index, name='index'),
    path('', views.NewsView.as_view(), name='index'),
    path('detail/', views.NewsDetailView.as_view(), name="detail"),
]


