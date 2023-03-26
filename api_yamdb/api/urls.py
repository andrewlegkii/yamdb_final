from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    RegisterUser, ReviewViewSet, TakeToken, TitleViewSet,
                    UsersViewSet)

app_name = 'api'
v1_router = DefaultRouter()
v1_router.register('genres', GenreViewSet)
v1_router.register('categories', CategoryViewSet)
v1_router.register('titles', TitleViewSet)
v1_router.register('users', UsersViewSet, basename='users'),
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews',
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)


urlpatterns = [
    path('v1/auth/signup/', RegisterUser.as_view(), name='register_user'),
    path('v1/auth/token/', TakeToken.as_view(), name='take_token'),
    path('v1/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/', include(v1_router.urls)),
]
