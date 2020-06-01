from django.db import models
# from apps.user.models import MyUser


class NewsType(models.Model):
    """新闻类型"""
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class News(models.Model):
    """新闻"""
    title = models.CharField(max_length=100)
    category = models.ForeignKey('NewsType', on_delete=models.SET_NULL, null=True)
    thumbnail = models.URLField()
    des = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey('user.MyUser', on_delete=models.SET_NULL, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)



