from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse

from news.models import News, Comment

User = get_user_model()


class NewsViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
            name="Test User",
            phone_number="1234567890",
        )
        self.client.force_authenticate(user=self.user)

    def test_create_news(self):
        data = {"title": "Test News", "url": "http://example.com"}
        response = self.client.post(reverse("news-list"), data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        news = News.objects.get(title="Test News")
        self.assertEqual(news.user, self.user)

    def test_destroy_own_news(self):
        news = News.objects.create(title="Test News", url="http://example.com", user=self.user)

        response = self.client.delete(reverse("news-detail", args=[news.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(News.DoesNotExist):
            News.objects.get(id=news.id)

    def test_destroy_other_user_news(self):
        other_user = User.objects.create_user(username="otheruser", email="other@example.com", password="testpassword")
        news = News.objects.create(title="Test News", url="http://example.com", user=other_user)

        response = self.client.delete(reverse("news-detail", args=[news.id]))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(News.objects.filter(id=news.id).exists(), True)


class CommentsViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test-comment",
            email="test-comment@example.com",
            password="test-comment",
            name="Test User",
            phone_number="1234567890",
        )

        self.other_user = User.objects.create_user(username="otherusercomment", email="otherusercomment@example.com",
                                                   password="testpassword")

        self.news = News.objects.create(title='Test News', url='http://example.com')

        self.other_user_comment = Comment.objects.create(
            text='Other User Comment',
            user=self.other_user,
            news=self.news
        )

    def test_list_comments(self):
        response = self.client.get(reverse('comment-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_create_comment(self):
        data = {'text': 'New Comment', 'news': self.news.id}
        response = self.client.post(reverse('comment-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_destroy_other_user_comment(self):
        news = News.objects.create(title="Test News", url="http://example.com", user=self.user)
        other_user = User.objects.create_user(username="otheruser", email="other@example.com", password="testpassword")
        comment = Comment.objects.create(text="Test", news=news, user=other_user)

        response = self.client.delete(reverse("comment-detail", args=[comment.id]))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(News.objects.filter(id=news.id).exists(), True)
