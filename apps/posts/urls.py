from django.urls import path
from rest_framework_nested import routers
from .views import PostViewSet, CommentViewSet, CategoryViewSet, RegisterView, LoginView

# Routers
router = routers.SimpleRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'posts', PostViewSet, basename='post')

category_posts_router = routers.NestedSimpleRouter(router, r'categories', lookup='category')
category_posts_router.register(r'posts', PostViewSet, basename='category-posts')

post_comments_router = routers.NestedSimpleRouter(router, r'posts', lookup='post')
post_comments_router.register(r'comments', CommentViewSet, basename='post-comments')

urlpatterns = (
    router.urls +
    category_posts_router.urls +
    post_comments_router.urls + [
        path('register/', RegisterView.as_view(), name='register'),
        path('login/', LoginView.as_view(), name='login'),
    ]
)
