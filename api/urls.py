from django.urls import path
from rest_framework.permissions import AllowAny
from .views import CreateUserView, CustomObtainAuthToken, PasswordResetConfirmView, PasswordResetView, PostList, PostDetail, CommentList, CommentDetail, LogoutView

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('login/', CustomObtainAuthToken.as_view(permission_classes=[AllowAny]), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('posts/', PostList.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('posts/<int:post_id>/comments/', CommentList.as_view()),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='comment-detail'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]