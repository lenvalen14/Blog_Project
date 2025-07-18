from rest_framework_nested import routers
from .views import PostViewSet, CommentViewSet, CategoryViewSet

# Router cấp 1 cho các tài nguyên chính: Category, Post, Comment
router = routers.SimpleRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'posts', PostViewSet, basename='post')

# Router cấp 2 cho các tài nguyên lồng nhau
# Tạo một router lồng nhau cho 'posts' nằm trong 'categories'
# URL sẽ có dạng: /categories/{category_pk}/posts/
category_posts_router = routers.NestedSimpleRouter(router, r'categories', lookup='category')
category_posts_router.register(r'posts', PostViewSet, basename='category-posts')

# Tạo một router lồng nhau cho 'comments' nằm trong 'posts'
# URL sẽ có dạng: /posts/{post_pk}/comments/
post_comments_router = routers.NestedSimpleRouter(router, r'posts', lookup='post')
post_comments_router.register(r'comments', CommentViewSet, basename='post-comments')


# Kết hợp tất cả các URL patterns lại
urlpatterns = router.urls + category_posts_router.urls + post_comments_router.urls