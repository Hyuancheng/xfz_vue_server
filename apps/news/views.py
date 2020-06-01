from django.shortcuts import render
from django.views import View
from .models import News


class NewsView(View):
    """首页"""

    def get(self, request):
        # 查询所有新闻，并查出目录及作者信息，减少后续数据库查询次数
        news = News.objects.all().defer('content').select_related('category', 'author')
        content = {
            'news': news
        }
        return render(request, 'news/index.html', content)


class NewsDetailView(View):
    """新闻详情"""
    def get(self, request):
        new_id = request.GET.get('new_id')
        new = News.objects.select_related('category', 'author').get(id=new_id)
        content = {
            'new': new
        }
        return render(request, 'news/news_detail.html', content)

# class NewsSearchView(View):
#     """搜索"""
#
#     def get(self, request):
#         news = News.objects.all().defer('content').select_related('category', 'author')
#         content = {
#             'news': news
#         }
#         return render(request, 'search/search.html', content)
