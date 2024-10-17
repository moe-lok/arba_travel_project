from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'text', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'post', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        post = self.context['post']
        return Comment.objects.create(user=user, post=post, **validated_data)

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'image', 'caption', 'created_at', 'updated_at', 'comments']