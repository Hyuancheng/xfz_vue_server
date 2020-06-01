from django.urls import path
from .views import PayInfoView

app_name = 'payinfo'

urlpatterns = [
    path('', PayInfoView.as_view(), name='index'),
]







