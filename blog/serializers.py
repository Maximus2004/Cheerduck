from django.utils import timezone
from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.Serializer): # класс, который может перевести модели Django в python, чтобы потом перевести в json
    title = serializers.CharField(max_length=200)  # ограниченый размер переменной
    text = serializers.CharField()  # текст для поста
    published_date = serializers.DateTimeField(default=timezone.now)  # дата публикации (актуальность)
    good_date = serializers.DateTimeField(default=timezone.now)  # удобная дата проведения
    likes = serializers.IntegerField()
    author_id = serializers.IntegerField()

    def create(self, validated_data): # чтобы serializer знал что делать при вызове save() в views
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.published_date = validated_data.get('published_date', instance.published_date)
        instance.likes = validated_data.get('likes', instance.likes)
        instance.author_id = validated_data.get('author_id', instance.author_id)
        instance.save()
        return instance