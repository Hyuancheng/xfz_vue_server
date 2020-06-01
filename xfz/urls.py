
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from apps.news.views import NewsView

urlpatterns = [
    path('', NewsView.as_view(), name='index'),
    # path('admin/', admin.site.urls),
    path('news/', include('apps.news.urls', namespace='news')),
    path('user/', include('apps.user.urls', namespace='user')),
    path('cms/', include('apps.cms.urls', namespace='cms')),
    path('course/', include('apps.course.urls', namespace='course')),
    path('pay/', include('apps.payinfo.urls', namespace='payinfo')),
    path('ueditor/', include('apps.ueditor.urls', namespace='ueditor')),
    path('search/', include('haystack.urls', namespace='search')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

