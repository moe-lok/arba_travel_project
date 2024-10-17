from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Post, Comment
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

User = get_user_model()

class UserTests(APITestCase):
    def test_create_user(self):
        """
        Ensure we can create a new user and obtain a token.
        """
        url = reverse('register')
        data = {'email': 'test@example.com', 'name': 'Test User', 'password': 'testpass123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')

        # Test login
        url = reverse('login')
        data = {'username': 'test@example.com', 'password': 'testpass123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

class PostTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', name='Test User', password='testpass123')
        self.client.force_authenticate(user=self.user)

    def test_create_post_without_image(self):
        """
        Ensure we can create a new post without an image.
        """
        url = reverse('post-list')
        data = {'caption': 'Test post without image'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().caption, 'Test post without image')
        self.assertFalse(Post.objects.get().image)  # Check if the image field is empty

    def test_create_post_with_image(self):
        """
        Ensure we can create a new post with an image.
        """
        url = reverse('post-list')
        
        # Create a test image
        file = io.BytesIO()
        image = Image.new('RGB', size=(100, 100), color=(255, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        
        data = {'caption': 'Test post with image', 'image': file}
        response = self.client.post(url, data, format='multipart')
        
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data}")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().caption, 'Test post with image')
        self.assertTrue(Post.objects.get().image)

    def test_get_posts(self):
        """
        Ensure we can retrieve posts.
        """
        Post.objects.create(user=self.user, caption='Test post')
        url = reverse('post-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class CommentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', name='Test User', password='testpass123')
        self.post = Post.objects.create(user=self.user, caption='Test post')
        self.client.force_authenticate(user=self.user)

    def test_create_comment(self):
        """
        Ensure we can create a new comment.
        """
        url = reverse('comment-list')
        data = {'post': self.post.id, 'text': 'Test comment'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().text, 'Test comment')

    def test_get_comments(self):
        """
        Ensure we can retrieve comments.
        """
        Comment.objects.create(user=self.user, post=self.post, text='Test comment')
        url = reverse('comment-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

