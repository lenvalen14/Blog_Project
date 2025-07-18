from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import Post, Comment, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'content', 'create_at', 'author', 'post']
        read_only_fields = ['author', 'post']


class PostDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'image', 'author',
            'category', 'create_at', 'comments_count', 'comments'
        ]
        read_only_fields = ['author', 'comments_count', 'comments']

    @extend_schema_field(serializers.IntegerField())
    def get_comments_count(self, obj):
        return obj.comments.count()

class PostCreateUpdateSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'image', 'author', 'category']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
