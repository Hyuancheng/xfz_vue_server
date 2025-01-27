from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


app_name = 'user'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('captcha/', views.img_captcha, name='captcha'),
    path('code/', views.send_code, name='send_code'),
]


