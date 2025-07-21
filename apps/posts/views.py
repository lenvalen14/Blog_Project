from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.posts.models import Post, Comment, Category
from apps.posts.pagination import CommentsPagination
from apps.posts.permissions import IsAuthorOrReadOnly
from apps.posts.renderers import CustomResponseRenderer
from apps.posts.serializers import PostDetailSerializer, PostCreateUpdateSerializer, CommentSerializer, \
    CategorySerializer, UserSerializer, RegisterSerializer, LoginSerializer


# Create your views here.
@extend_schema(tags=["Users"])
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    renderer_classes = [CustomResponseRenderer]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "Registered successfully",
            "data": self.get_serializer(user).data
        }, status=status.HTTP_201_CREATED)

@extend_schema(tags=["Users"])
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    renderer_classes = [CustomResponseRenderer]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({
            "message": "Logged in successfully",
            "data": serializer.validated_data
        }, status=status.HTTP_200_OK)

@extend_schema(tags=["Posts"])
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    pagination_class = PageNumberPagination
    renderer_classes = [CustomResponseRenderer]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        return Response({
            "message": "Created post successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


@extend_schema(tags=['Comments'])
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = CommentsPagination
    renderer_classes = [CustomResponseRenderer]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

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
    pagination_class = PageNumberPagination
    renderer_classes = [CustomResponseRenderer]
    permission_classes = [IsAuthenticatedOrReadOnly]

@extend_schema(tags=['Users'])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer