from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import Post, Comment, User
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.conf import settings
import logging
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CreateUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'user': UserSerializer(user).data,
                'message': 'User created successfully',
            }, status=status.HTTP_201_CREATED)
        logger.error(f"User registration failed. Errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        logger.debug(f"Full request data: {request.data}")
        logger.debug(f"Request headers: {request.headers}")
        
        email = request.data.get('email')
        password = request.data.get('password')
        logger.debug(f"Login attempt for email: {email}")
        
        user = authenticate(request, email=email, password=password)
        logger.debug(f"Authentication result: {'Success' if user else 'Failure'}")
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            logger.debug(f"Token created: {created}")
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            })
        logger.warning(f"Invalid credentials for email: {email}")
        return Response({'error': 'Invalid Credentials'}, status=400)
    
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # Simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, post_id=self.kwargs['post_id'])

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PasswordResetView(APIView):
    permission_classes = ()

    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
            send_mail(
                'Password Reset',
                f'Click the following link to reset your password: {reset_link}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
        return Response({"message": "If an account with this email exists, a password reset link has been sent."}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(APIView):
    permission_classes = ()

    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            new_password = request.data.get('new_password')
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid reset link."}, status=status.HTTP_400_BAD_REQUEST)
