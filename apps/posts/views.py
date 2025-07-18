from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser

from apps.posts.models import Post, Comment, Category
from apps.posts.serializers import PostDetailSerializer, PostCreateUpdateSerializer, CommentSerializer, \
    CategorySerializer, UserSerializer


# Create your views here.
@extend_schema(tags=["Posts"])
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = PostCreateUpdateSerializer

    def get_queryset(self):
        if 'category_pk' in self.kwargs:
            category_pk = self.kwargs['category_pk']
            category = get_object_or_404(Category, pk=category_pk)
            return Post.objects.filter(category=category)
        return super().get_queryset()

    def get_serializer_context(self):
        return {'request': self.request}

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer
        return PostDetailSerializer

    @extend_schema(
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'title': {'type': 'string'},
                    'content': {'type': 'string'},
                    'category': {'type': 'integer'},
                    'image': {'type': 'string', 'format': 'binary'}
                },
                'required': ['title', 'content', 'category']
            }
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

@extend_schema(tags=['Comments'])
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_pk = self.kwargs['post_pk']
        return Comment.objects.filter(post_id=post_pk)

    def perform_create(self, serializer):
        post_pk = self.kwargs['post_pk']
        post = get_object_or_404(Post, pk=post_pk)
        serializer.save(author=self.request.user, post=post)

@extend_schema(tags=['Categories'])
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

@extend_schema(tags=['Users'])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer