from rest_framework import serializers
from .models import NewsType, News


class NewsTypeListSerializer(serializers.ModelSerializer):
    news_count = serializers.IntegerField()

    class Meta:
        model = NewsType
        fields = '__all__'


class NewsTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsType
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    category = NewsTypeSerializer()
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = News
        fields = '__all__'


class NewsListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = News
        fields = ('id', 'category', 'author', 'pub_date', 'title')
